# RichTextEditor customization:
#   See https://docs.wagtail.io/en/v2.7/advanced_topics/customisation/extending_draftail.html
#   And https://medium.com/@timlwhite/custom-in-line-styles-with-draftail-939201c2bbda

from django.core.cache import cache

# The real code runs "instance.sync_trees()" here, but we want this to do nothing instead,
# so that locale creation creates the locale entry but does not try to sync 1300+ pages as
# part of the same web request.
from django.db.models.signals import post_save
from django.templatetags.static import static
from django.urls import reverse
from django.utils.html import escape
from wagtail import hooks
from wagtail.admin.menu import MenuItem
from wagtail.admin.rich_text.converters.html_to_contentstate import (
    InlineStyleElementHandler,
)
from wagtail.admin.rich_text.editors.draftail import features as draftail_features
from wagtail.coreutils import find_available_slug
from wagtail.rich_text import LinkHandler
from wagtail_localize.models import (
    LocaleSynchronization,
    sync_trees_on_locale_sync_save,
)
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup
from wagtail.snippets.models import register_snippet

from networkapi.wagtailpages.pagemodels.buyersguide.homepage import BuyersGuidePage
from networkapi.wagtailpages.pagemodels.buyersguide.products import ProductPage
from networkapi.wagtailpages.utils import get_locale_from_request
from networkapi.wagtailpages import models as wagtailpages_models

post_save.disconnect(sync_trees_on_locale_sync_save, sender=LocaleSynchronization)


# Extended rich text features for our site
@hooks.register("register_rich_text_features")
def register_large_feature(features):
    """
    Registering the 'large' Draftail feature which
    adds a span around the selected text with its class
    set to 'tw-body-large'
    """

    # 1. Set up variables for use below
    feature_name = "large"
    type_ = "LARGE"

    # 2. Set up a dictionary to pass to Draftail to configure
    # how it handles this feature in its toolbar.
    # The 'style' attribute controls how Draftail formats that text
    # in the editor - does not affect the final rendered HTML
    # In this case, I am adding similar formatting to what
    # the CSS will do to that 'small-caption' class in the template
    control = {
        "type": type_,
        "label": "L",
        "description": "Large body text",
        "style": {"font-size": "125%"},
    }

    # 3. Call register_editor_plugin to register the configuration for Draftail.
    features.register_editor_plugin("draftail", feature_name, draftail_features.InlineStyleFeature(control))

    # 4.configure the content transform from the DB to the editor and back.

    # The "From" version uses a CSS selector to find spans with a class of 'tw-body-large'
    # The "To" version adds a span with a class of 'tw-body-large' surrounding the selected text
    db_conversion = {
        "from_database_format": {'span[class="tw-body-large"]': InlineStyleElementHandler(type_)},
        "to_database_format": {"style_map": {type_: 'span class="tw-body-large"'}},
    }

    # 5. Call register_converter_rule to register the content transformation conversion.
    features.register_converter_rule("contentstate", feature_name, db_conversion)

    # 6. (optional) Add the feature to the default features list to make it available
    # on rich text fields that do not specify an explicit 'features' list
    features.default_features.append("large")


# Updating external links in rich text blocks to open in a new tab
class RichTextExternalLinkNewTabHandler(LinkHandler):
    identifier = "external"

    @classmethod
    def expand_db_attributes(cls, attrs):
        href = attrs["href"]
        return '<a href="%s" target="_blank">' % escape(href)


@hooks.register("register_rich_text_features")
def register_external_rich_text_link(features):
    features.register_link_type(RichTextExternalLinkNewTabHandler)


# Ensure that pages in the PageChooserPanel listings are ordered on most-recent-ness
@hooks.register("construct_page_chooser_queryset")
def order_pages_in_chooser(pages, request):
    # Change listings in the "page chooser" modal:
    if "choose-page" in request.path:
        return pages.order_by("-first_published_at")

    # Don't change search results (shown in ./admin/pages/search)
    return pages


@hooks.register("before_delete_page")
def before_delete_page(request, page):
    """Delete PNI votes when a product is deleted."""
    if isinstance(page, ProductPage) and page.votes:
        # Delete the vote from ProductPages
        page.votes.delete()


@hooks.register("after_delete_page")
@hooks.register("after_publish_page")
@hooks.register("after_unpublish_page")
def manage_pni_cache(request, page):
    if isinstance(page, ProductPage) or isinstance(page, BuyersGuidePage):
        # Clear all of our Django-based cache.
        # This is easier than looping through every Category x Language Code available
        # To specifically clear PNI-based cache.
        cache.clear()


@hooks.register("after_publish_page")
def sync_localized_slugs(request, page):
    for translation in page.get_translations():
        translation.slug = find_available_slug(translation.get_parent(), page.slug, ignore_page_id=translation.id)

        if translation.alias_of_id is not None:
            # This is still an alias rather than a published
            # localized page, so we can only save it as we
            # would any plain Django model:
            translation.save()

        else:
            # If it's a real page, it needs to go through
            # the revision/publication process.
            translation.save_revision().publish()


@hooks.register("after_delete_page")
@hooks.register("after_publish_page")
@hooks.register("after_unpublish_page")
def manage_index_pages_cache(request, page):
    """
    TODO: remove this check and associated caching when we switch over to
          proper "related posts" in the CMS for blog pages and campaigns.
    """
    parent = page.get_parent().specific
    locale = get_locale_from_request(request)

    if hasattr(parent, "clear_index_page_cache"):
        parent.clear_index_page_cache(locale)


@hooks.register("insert_global_admin_js", order=100)
def global_admin_js():
    """Add /static/css/custom.js to the admin."""
    max_length_js = static("wagtailadmin/js/max-length-field.js")
    return f'<script src="{max_length_js}"></script>'


@hooks.register("insert_global_admin_css")
def global_admin_css():
    max_length_css = static("wagtailadmin/css/max-length-field.css")
    return f'<link rel="stylesheet" href="{max_length_css}">'


@hooks.register("register_icons")
def register_icons(icons):
    return icons + [
        "icons/arrows-up-down.svg",
        "icons/tito.svg",
        "icons/ticket.svg",
        "icons/newspaper.svg",
        "icons/mozfest.svg",
    ]


class HowToWagtailMenuItem(MenuItem):
    def is_shown(self, request):
        return True


@hooks.register("register_admin_menu_item")
def register_howto_menu_item():
    return HowToWagtailMenuItem(
        "How Do I Wagtail",
        reverse("how-do-i-wagtail"),
        name="howdoIwagtail",
        classname="icon icon-help",
        order=1000,
    )


class BlogPageTopicSnippetViewSet(SnippetViewSet):
    model = wagtailpages_models.BlogPageTopic
    icon = "tag"
    menu_order = 000
    menu_label = "Topics"
    menu_name = "Topics"
    list_display = ("name",)
    search_fields = ("name", "title", "intro", "share_description")


class BlogSignupSnippetViewSet(SnippetViewSet):
    model = wagtailpages_models.BlogSignup
    icon = "newspaper"
    menu_order = 100
    menu_label = "Newsletter Signups"
    menu_name = "Newsletter Signups"
    list_display = (
        "name",
        "newsletter",
    )
    search_fields = ("name", "header", "description", "newsletter")


class BlogViewSetGroup(SnippetViewSetGroup):
    items = (BlogPageTopicSnippetViewSet, BlogSignupSnippetViewSet)
    menu_icon = "bold"
    menu_label = "Blog"
    menu_name = "Blog"
    menu_order = 1400


register_snippet(BlogViewSetGroup)
