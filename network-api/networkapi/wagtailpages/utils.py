import re

from bs4 import BeautifulSoup

from itertools import chain
from django.apps import apps
from django.conf import settings
from django.db.models import Count
from django.urls import LocalePrefixPattern, URLResolver
from django.utils.text import slugify
from django.utils.translation import gettext
from django.utils.translation.trans_real import (
    check_for_language, get_languages, get_language_from_path,
    get_supported_language_variant, parse_accept_lang_header, language_code_re
)
from sentry_sdk import capture_exception


def titlecase(s):
    '''
    See https://docs.python.org/3.7/library/stdtypes.html#str.title
    for why this definition exists (basically: apostrophes)
    '''
    return re.sub(
        r"[A-Za-z]+('[A-Za-z]+)?",
        lambda mo: mo.group(0)[0].upper() +
        mo.group(0)[1:].lower(),
        s
    )


def set_main_site_nav_information(page, context, homepage_class_name):
    '''
    Find the homepage, and then record all pages that should end up as nav items. Note
    that subclasses can bypass this, because the MozfestHomepage doesn't need any of
    this work to be done.
    '''

    root = list(filter(
        lambda x: x.specific.__class__.__name__ == homepage_class_name,
        page.get_ancestors(True)  # incude ourselves!
    ))[0]

    context['menu_root'] = root
    context['menu_items'] = root.get_children().live().in_menu()
    return context


def get_page_tree_information(page, context):
    '''
    Helper function for abstracting details about page trees
    of the same type. Information returned is:
    - what the root of the tree is
    - what the root page's title is
    - whether the reference page is the tree root
    - whether this is a singleton "tree"
    '''

    ancestors = page.get_ancestors()
    root = next((n for n in ancestors if n.specific_class == page.specific_class), page)
    context['root'] = root

    is_top_page = (root == page)
    context['is_top_page'] = is_top_page

    children = page.get_children().live()
    has_children = len(children) > 0
    context['singleton_page'] = (is_top_page and not has_children)

    mchildren = root.get_children().live().in_menu()
    context['uses_menu'] = len(mchildren) > 0

    return context


def get_descendants(node, list, authenticated=False, depth=0, max_depth=2):
    '''
    helper function to get_menu_pages for performing a depth-first
    discovery pass of all menu-listable children to some root node.
    '''
    if (depth <= max_depth):
        title = node.title
        header = getattr(node.specific, 'header', None)
        if header:
            title = header
        menu_title = title if depth > 0 else gettext('Overview')
        restriction = node.get_view_restrictions().first()
        try:
            restriction_type = restriction.restriction_type
        except AttributeError:
            restriction_type = None

        list.append({
            'page': node,
            'menu_title': menu_title,
            'depth': depth,
            'restriction': restriction_type,
        })

        nextset = node.get_children().in_menu()

        # Do not show draft/private pages to users who are
        # not logged into the CMS itself.
        if authenticated is False:
            nextset = nextset.live().public()

        for child in nextset:
            get_descendants(child, list, authenticated, depth + 1)


def get_menu_pages(root, authenticated=False):
    '''
    convenience function for getting all (menu listable) child
    pages for some root node.
    '''
    menu_pages = list()
    get_descendants(root, menu_pages, authenticated)
    return menu_pages


def get_mini_side_nav_data(context, page, no_minimum_page_count=False):
    user = context['user']
    authenticated = user.is_authenticated if user else False
    menu_pages = get_menu_pages(context['root'], authenticated)

    # We need at least 2 pages, or a nav menu is meaningless.
    if no_minimum_page_count is False and len(menu_pages) < 2:
        menu_pages = False

    # Return the list of values we need to have our template
    # generate the appropriate sidebar HTML.
    return {
        'singleton_page': context['singleton_page'],
        'current': page,
        'menu_pages': menu_pages,
    }


def get_content_related_by_tag(page, result_count=3):
    """
    Get all posts that feel related to this page, based
    on its `.tags` content. If it has tags.
    """

    if hasattr(page.specific, 'tags') is False:
        return list()

    page_models_with_tags = (
        apps.get_model('wagtailpages', 'BlogPage'),
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

    for page_type in page_models_with_tags:
        # get all pages that share tags with this page
        related_pages = page_type.objects.filter(tags__in=own_tags).live()

        # Exlude "this page" from the result set for the page's own page type
        # so that we don't end up with "this page is most similar to itself".
        if page.__class__ is page_type:
            related_pages = related_pages.exclude(pk=page.pk)

        # Annotate the results by adding a column that, effectively, records
        # a `countDistinct(result_table.tag)` for each related post.
        annotated = related_pages.annotate(num_common_tags=Count('pk'))

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
            reverse=True
        )
    except TypeError as err:
        capture_exception(err)

    return result_list[:result_count]


def insert_panels_after(panels, after_label, additional_panels):
    """
    Insert wagtail panels somewhere in another set of panels
    """
    position = next(
        (i for i, item in enumerate(panels) if item.heading == after_label),
        None
    )

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
            return path[len(language_prefix):], (), {}
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
    language, _, country = language.lower().partition('-')
    if country:
        return language + '-' + country.upper()
    return language


def get_language_from_request(request, check_path=False):
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

    accept = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
    for accept_lang, unused in parse_accept_lang_header(accept):
        if accept_lang == '*':
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
    body = stream_data.__dict__['stream_data']
    data = {}
    headers = []
    for block in body:
        if not request.is_preview:
            # Check for live versions of the page first because these will be served
            # much more frequently than preview pages.
            # In live pages (not previewed) we have a block `type` and block `value`.
            # In preview pages, we have a tuple where the first value is the block['type']
            # and the second value is the block['value']
            for block in body:
                if block['type'] == stream_block_name:
                    soup = BeautifulSoup(block['value'], 'html.parser')
                    _headers = soup.findAll('h2')
                    for _h in _headers:
                        headers.append(_h.get_text())
        else:
            # If the page is a preview, look for live streamfield data.
            # Previewed streamfield is stored differently than live streamfield data; as a tuple
            # And thus we check if the first value is the block name, and the second value in
            # the tuple is going to be the actual block data.
            if block[0] == stream_block_name:
                soup = BeautifulSoup(str(block[1]), 'html.parser')
                _headers = soup.findAll('h2')
                for _h in _headers:
                    headers.append(_h.text)
    data = {
        slugify(header): header for header in headers
    }
    return tuple(data.items())
