import ntpath
import re
from io import BytesIO
from itertools import chain
from mimetypes import MimeTypes
from typing import Optional

import requests
from bs4 import BeautifulSoup
from django import forms
from django.apps import apps
from django.conf import settings
from django.core.files.images import ImageFile
from django.db import models
from django.db.models import Count, QuerySet
from django.urls import LocalePrefixPattern, URLResolver
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.utils.translation import gettext
from django.utils.translation.trans_real import (
    check_for_language,
    get_language_from_path,
    get_languages,
    get_supported_language_variant,
    language_code_re,
    parse_accept_lang_header,
)
from PIL import Image as PILImage
from sentry_sdk import capture_exception
from wagtail.images import get_image_model
from wagtail.models import Collection, Locale, PageViewRestriction

from networkapi.images.models import FoundationCustomImage
from networkapi.wagtailpages.pagemodels.profiles import Profile

Image = get_image_model()


def titlecase(s):
    """
    See https://docs.python.org/3.7/library/stdtypes.html#str.title
    for why this definition exists (basically: apostrophes)
    """
    return re.sub(
        r"[A-Za-z]+('[A-Za-z]+)?",
        lambda mo: mo.group(0)[0].upper() + mo.group(0)[1:].lower(),
        s,
    )


def set_main_site_nav_information(page, context, homepage_class_name):
    """
    Find the homepage, and then record all pages that should end up as nav items. Note
    that subclasses can bypass this, because the MozfestHomepage doesn't need any of
    this work to be done.
    """

    root = list(
        filter(
            lambda x: x.specific.__class__.__name__ == homepage_class_name,
            page.get_ancestors(True),  # incude ourselves!
        )
    )[0]

    context["menu_root"] = root
    context["menu_items"] = root.get_children().live().in_menu()
    return context


def get_page_tree_information(page, context):
    """
    Helper function for abstracting details about page trees
    of the same type. Information returned is:
    - what the root of the tree is
    - what the root page's title is
    - whether the reference page is the tree root
    - whether this is a singleton "tree"
    """

    ancestors = page.get_ancestors()
    root = next((n for n in ancestors if n.specific_class == page.specific_class), page)
    context["root"] = root

    is_top_page = root == page
    context["is_top_page"] = is_top_page

    children = page.get_children().live()
    has_children = len(children) > 0
    context["singleton_page"] = is_top_page and not has_children

    mchildren = root.get_children().live().in_menu()
    context["uses_menu"] = len(mchildren) > 0

    return context


def get_descendants(node, list, authenticated=False, depth=0, max_depth=2):
    """
    helper function to get_menu_pages for performing a depth-first
    discovery pass of all menu-listable children to some root node.
    """
    if depth <= max_depth:
        title = node.title
        header = getattr(node.specific, "header", None)
        if header:
            title = header
        menu_title = title if depth > 0 else gettext("Overview")
        restriction = node.get_view_restrictions().first()
        try:
            restriction_type = restriction.restriction_type
        except AttributeError:
            restriction_type = None

        list.append(
            {
                "page": node,
                "menu_title": menu_title,
                "depth": depth,
                "restriction": restriction_type,
            }
        )

        nextset = node.get_children().in_menu()

        # Do not show draft/private pages to users who are
        # not logged into the CMS itself.
        if authenticated is False:
            nextset = nextset.live().public()

        for child in nextset:
            get_descendants(child, list, authenticated, depth + 1)


def get_menu_pages(root, authenticated=False):
    """
    convenience function for getting all (menu listable) child
    pages for some root node.
    """
    menu_pages = list()
    get_descendants(root, menu_pages, authenticated)
    return menu_pages


def get_mini_side_nav_data(context, page, no_minimum_page_count=False):
    user = context["user"]
    authenticated = user.is_authenticated if user else False
    menu_pages = get_menu_pages(context["root"], authenticated)

    # We need at least 2 pages, or a nav menu is meaningless.
    if no_minimum_page_count is False and len(menu_pages) < 2:
        menu_pages = False

    # Return the list of values we need to have our template
    # generate the appropriate sidebar HTML.
    return {
        "singleton_page": context["singleton_page"],
        "current": page,
        "menu_pages": menu_pages,
    }


def get_content_related_by_tag(page, result_count=3):
    """
    Get all posts that feel related to this page, based
    on its `.tags` content. If it has tags.
    """

    if hasattr(page.specific, "tags") is False:
        return list()

    page_models_with_tags = (
        apps.get_model("wagtailpages", "BlogPage"),
        #
        # Uncomment the following class(es) to add them to the
        # set of classes to use for tag matching:
        #
        # apps.get_model('wagtailpages', 'BanneredCampaignPage'),
        # apps.get_model('wagtailpages', 'CampaignPage'),
        # apps.get_model('wagtailpages', 'OpportunityPage'),
    )

    results = False
    own_tags = page.tags.all()
    own_locale = page.locale

    for page_type in page_models_with_tags:
        # Get all pages that share tags with this page
        related_pages = page_type.objects.filter(tags__in=own_tags).live()

        # Filter related pages to be of same locale as reference page
        if own_locale:
            related_pages = related_pages.filter(locale=own_locale)

        # Exlude "this page" from the result set for the page's own page type
        # so that we don't end up with "this page is most similar to itself".
        if page.__class__ is page_type:
            related_pages = related_pages.exclude(pk=page.pk)

        # Annotate the results by adding a column that, effectively, records
        # a `countDistinct(result_table.tag)` for each related post.
        annotated = related_pages.annotate(num_common_tags=Count("pk"))

        if results is False:
            results = annotated
        else:
            results = chain(results, annotated)

    # Finally, we sort on those tag count values, with publication
    # date as secondary sorting, so that "the same number of matching
    # tags" is further sorted such that the most recent post shows
    # up first (note that this is done on the database side, not in python).

    # FIXME: temporary try/except to figure out a bug in production:
    # See https://github.com/mozilla/foundation.mozilla.org/issues/4046

    result_list = list(results)

    try:
        result_list = sorted(
            result_list,
            key=lambda p: (p.num_common_tags, p.last_published_at),
            reverse=True,
        )
    except TypeError as err:
        capture_exception(err)

    return result_list[:result_count]


def insert_panels_after(panels, after_label, additional_panels):
    """
    Insert wagtail panels somewhere in another set of panels
    """
    position = next((i for i, item in enumerate(panels) if item.heading == after_label), None)

    if position is not None:
        cut = position + 1
        panels = panels[0:cut] + additional_panels + panels[cut:]
    else:
        raise ValueError(f'No panel with heading "{after_label}" in panel list')

    return panels


class ISO3166LocalePrefixPattern(LocalePrefixPattern):
    """LocalePrefixPattern subclass that enforces URL prefixes in the form en-US"""

    def match(self, path):
        language_prefix = language_code_to_iso_3166(self.language_prefix)
        if path.startswith(language_prefix):
            return path[len(language_prefix) :], (), {}
        return None


def i18n_patterns(*urls, prefix_default_language=True):
    """
    Replacement for django.conf.urls.i18_patterns that uses ISO3166LocalePrefixPattern
    instead of django.urls.resolvers.LocalePrefixPattern.
    """
    if not settings.USE_I18N:
        return list(urls)
    return [
        URLResolver(
            ISO3166LocalePrefixPattern(prefix_default_language=prefix_default_language),
            list(urls),
        )
    ]


def language_code_to_iso_3166(language):
    """Turn a language name (en-us) into an ISO 3166 format (en-US)."""
    language, _, country = language.lower().partition("-")
    if country:
        return language + "-" + country.upper()
    return language


def get_locale_from_request(request, check_path=True):
    language_code = get_language_from_request(request, check_path)

    try:
        return Locale.objects.get(language_code=language_code)
    except Locale.DoesNotExist:
        return Locale.objects.get(language_code=settings.LANGUAGE_CODE)


def get_language_from_request(request, check_path=True):
    """
    Replacement for django.utils.translation.get_language_from_request.
    The portion of code that is modified is identified below with a comment.
    """
    if check_path:
        lang_code = get_language_from_path(request.path_info)
        if lang_code is not None:
            return lang_code

    lang_code = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME)
    if lang_code is not None and lang_code in get_languages() and check_for_language(lang_code):
        return lang_code

    try:
        return get_supported_language_variant(lang_code)
    except LookupError:
        pass

    accept = request.headers.get("accept-language", "")
    for accept_lang, unused in parse_accept_lang_header(accept):
        if accept_lang == "*":
            break

        # Convert lowercase region to uppercase before attempting to find a variant.
        # This is the only portion of code that is modified from the core function.
        accept_lang = language_code_to_iso_3166(accept_lang)

        if not language_code_re.search(accept_lang):
            continue

        try:
            return get_supported_language_variant(accept_lang)
        except LookupError:
            continue

    try:
        return get_supported_language_variant(settings.LANGUAGE_CODE)
    except LookupError:
        return settings.LANGUAGE_CODE


def localize_queryset(
    queryset, preserve_order=False, include_draft_translations=False, include_only_translations=False
):
    """
    Return a localized version of this queryset.

    A localized queryset is one where objects are replaced with versions translated
    into the active locale. Where a translation isn't available for an object, the
    original is retained instead.

    By default, the same ordering definition as in the original queryset is applied.
    This means that the translated values are being considered during ordering,
    which can lead to a different order than the original queryset. If you want to
    preserve the same order as the original queryset, you need to pass
    ``preserve_order=True``.

    If a model inherits from
    :py:class:`DraftStateMixin <wagtail.models.DraftStateMixin>`,
    draft translations are not considered as translated instances. If a translation
    is in draft, the original instance is used instead. To override this behavior
    and include draft translations, pass ``include_draft_translations=True``.

    By default, the localized queryset can contain untranslated instances from the
    original queryset if no translation for the instance is available. If this is
    not desired, pass ``include_only_translations=True`` to only include instances
    that are translated into the active locale.

    Note: Because this method uses a complex query to retrieve the items in the
    localized queryset, effects of methods like `annotate`, `select_related` and
    `prefetch_related` will be reapplied to the localized queryset. However, this
    means that the values will be recomputed with the translated values. This can
    lead to unexpected results.

    Extracted from https://github.com/wagtail/wagtail/pull/11274
    """
    # Get all instances that are available in the active locale. We can find these
    # by getting all model instances that have a translation key from the original
    # queryset and that are available in the active locale.
    active_locale = Locale.get_active()
    original_translation_keys = queryset.values_list("translation_key", flat=True)
    translated_instances = queryset.model.objects.filter(
        locale_id=active_locale.pk,
        translation_key__in=original_translation_keys,
    )

    # Don't consider draft translations. If a translation is in draft, we want to
    # use the original instance instead. To do so, we exclude draft translations.
    # This only applies if the model has a `live` field. We allow bypassing this
    # behavior by passing `include_draft_translations=True`.
    from wagtail.models import DraftStateMixin

    if issubclass(queryset.model, DraftStateMixin) and not include_draft_translations:
        translated_instances = translated_instances.exclude(live=False)

    if include_only_translations:
        # If we only want to include translations, we can use the translated
        # instances as the localized queryset.
        localized_queryset = translated_instances
    else:
        # Otherwise, we need to combine the translated instances with the
        # untranslated instance.

        # Get all instances that are not available in the active locale, these are
        # the untranslated instances. We can find these by excluding the translation
        # keys for which translations exist from the original queryset.
        translated_translation_keys = translated_instances.values_list("translation_key", flat=True)
        untranslated_instances = queryset.exclude(
            translation_key__in=translated_translation_keys,
        )

        # Combine the translated and untranslated querysets to get the localized
        # queryset.
        localized_queryset = queryset.model.objects.filter(
            models.Q(pk__in=translated_instances) | models.Q(pk__in=untranslated_instances)
        )

    if annotations := queryset.query.annotations:
        localized_queryset = localized_queryset.annotate(**annotations)

    if not preserve_order:
        # Apply the same `order_by` as in the original queryset. This does not mean
        # that the order of the items is retained. Rather, the same fields are used
        # for ordering. However, the ordering is likely to be different because the
        # translated values are used.
        return localized_queryset.order_by(*queryset.query.order_by)

    else:
        # Keep the same order as in the original queryset. To do so, we annotate the
        # localized queryset with the original order of the translation keys, and
        # then order by that annotation.
        ordering_when_clauses = [
            models.When(translation_key=tk, then=models.Value(index))
            for index, tk in enumerate(original_translation_keys)
        ]
        if ordering_when_clauses:
            localized_annotated_queryset = localized_queryset.annotate(
                original_order=models.Case(*ordering_when_clauses)
            )
            return localized_annotated_queryset.order_by("original_order")
        else:
            return localized_queryset


def map_language_code_to_tito_supported_language_code(language_code: str) -> str:
    """
    Return the Tito supported language code for the given language code.

    Checks if the supplied language code is currently supported by Tito. If not, default to English, to prevent the
    Tito widget from crashing due to an unsupported language.

    For more info see: https://github.com/mozilla/foundation.mozilla.org/issues/9790
    """
    tito_supported_language_codes = ["en", "de", "es", "fr", "nl", "pl", "sw"]
    default_language_code = settings.LANGUAGE_CODE

    if language_code in tito_supported_language_codes:
        return language_code
    else:
        return default_language_code


def get_plaintext_titles(request, stream_data, stream_block_name):
    """
    Accepts a StreamField and the name of a streamblock to look for,
    parses the data for <h2> elements, strips all HTML tags,
    and creates a dictionary of slugs to headers.

    :stream_data is the StreamField object (not the raw json that's stored)
    :stream_block_name is the name of the StreamField block associated with
                        the richtext field.

    Example dictionary that's created:
    {
        'hello-world': 'Hello World',
        'second-title-here': 'Second Title Here',
    }

    Example return output:
    (
        ('hello-world', 'Hello World'),
        ('second-title-here', 'Second Title Here')
    )
    """
    data = {}
    headers = []
    for block in stream_data:
        if block.block_type == stream_block_name:
            soup = BeautifulSoup(str(block.value), "html.parser")
            _headers = soup.findAll("h2")
            for _h in _headers:
                headers.append(_h.get_text())
    data = {slugify(header): header for header in headers}
    return tuple(data.items())


def create_wagtail_image(
    img_src: str, image_name: Optional[str] = None, collection_name: Optional[str] = None
) -> Optional[FoundationCustomImage]:
    """
    Create a Wagtail Image from a given source. It takes an optional file name
    and collection name.

    If the collection name is provided, but a collection is not found, a new collection
    will be created.

    Examples:
        create_wagtail_image('/app/source/images/myimage.jpg')
        create_wagtail_image('/app/source/images/myimage.jpg', image_name='Same Image.jpg')
        create_wagtail_image('/app/source/images/myimage.jpg', collection_name='Dev test collection')
    """

    mime = MimeTypes()
    guessed_mime_type = mime.guess_type(img_src)

    if guessed_mime_type and guessed_mime_type[0]:
        mime_type = guessed_mime_type[0].split("/")[1].upper()
    else:
        # Default to a JPEG mimetype.
        mime_type = "JPEG"

    f = BytesIO()

    # Copy the image to the local machine before converting it to a Wagtail image.
    if img_src.startswith("http"):
        # Download the image from a URL. Requires the requests package.
        response = requests.get(img_src, stream=True)
        if response.status_code == 200:
            # Create an image out of a web resource URL and write it to a PIL Image.
            pil_image = PILImage.open(response.raw)
            pil_image.save(f, mime_type)
        else:
            # Image URL didn't 200 for us. Nothing we can do about that. Return early.
            print(f"Could not generate image from url {img_src}")
            return None
    else:
        # Save the image from a local source. The requests package is not needed.
        pil_image = PILImage.open(img_src)
        pil_image.save(f, mime_type)

    # If the image is supposed to be part of a collection, look for the collection or create it.
    collection = Collection.get_first_root_node()
    if collection_name:
        specific_collection = Collection.objects.filter(name=collection_name).first()
        # Use the specific collection if it's found. Otherwise create a new collection
        # based on the `collection_name` parameter.
        collection = specific_collection if specific_collection else collection.add_child(name=collection_name)

    # If an image name was not provided, create one from the img_src..
    if not image_name:
        image_name = ntpath.basename(img_src)

    # Create the Wagtail Image and return it
    wagtail_image = Image.objects.create(title=image_name, file=ImageFile(f, name=image_name), collection=collection)
    return wagtail_image


class CharCountWidget(forms.TextInput):
    def render(self, name, value, attrs=None, renderer=None):
        html = super().render(name, value, attrs)
        inline_code = mark_safe("<h3 class='max-length-countdown'></h3>")
        return html + inline_code


def get_default_locale():
    """
    We defer this logic to a function so that we can call it on demand without
    running into "the db is not ready for queries yet" problems.
    """
    DEFAULT_LOCALE = Locale.objects.get(language_code=settings.LANGUAGE_CODE)
    DEFAULT_LOCALE_ID = DEFAULT_LOCALE.id
    return (
        DEFAULT_LOCALE,
        DEFAULT_LOCALE_ID,
    )


def get_blog_authors(profiles: "QuerySet[Profile]") -> "QuerySet[Profile]":
    """Filter a queryset of profiles to only those who are blog authors."""
    return profiles.filter(blogauthors__isnull=False).distinct()


def sync_view_restriction_change(sender, instance, **kwargs):
    """
    Syncs a page's view restriction changes to all locales.
    """
    page = instance.page.specific
    all_pages = [page]

    # Only sync view restriction changes from the default locale.
    if page.locale.is_default:
        view_restrictions = page.view_restrictions.all()
        translations = page.get_translations(inclusive=False)

        for translation in translations:
            translation.view_restrictions.all().delete()
            for restriction in view_restrictions:
                new_restriction = PageViewRestriction.objects.create(
                    page=translation,
                    restriction_type=restriction.restriction_type,
                    password=restriction.password,
                )
                new_restriction.groups.set(restriction.groups.all())

            # Add translation to list in case we need to clear index cache later
            all_pages.append(translation)

    parent = page.get_parent().specific
    # If this page lives under a cacheable index page, clear its cache for all locales.
    # This ensures index listings reflect the current visibility of all pages.
    if hasattr(parent, "clear_index_page_cache"):
        for p in all_pages:
            index_page = p.get_parent().specific
            index_page.clear_index_page_cache(p.locale)
