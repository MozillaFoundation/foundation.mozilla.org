# RichTextEditor customization:
#   See https://docs.wagtail.io/en/v2.7/advanced_topics/customisation/extending_draftail.html
#   And https://medium.com/@timlwhite/custom-in-line-styles-with-draftail-939201c2bbda

from django.core.cache import cache
from django.db.models import Prefetch

# The real code runs "instance.sync_trees()" here, but we want this to do nothing instead,
# so that locale creation creates the locale entry but does not try to sync 1300+ pages as
# part of the same web request.
from django.db.models.signals import post_save
from django.shortcuts import redirect
from django.templatetags.static import static
from django.urls import reverse
from django.utils.html import escape
from wagtail import hooks
from wagtail.admin import messages
from wagtail.admin.menu import MenuItem
from wagtail.admin.rich_text.converters.html_to_contentstate import (
    InlineStyleElementHandler,
)
from wagtail.admin.rich_text.editors.draftail import features as draftail_features
from wagtail.admin.ui.tables import BooleanColumn
from wagtail.contrib.settings.models import register_setting
from wagtail.contrib.settings.registry import SettingMenuItem
from wagtail.coreutils import find_available_slug
from wagtail.rich_text import LinkHandler
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup
from wagtail_ab_testing.events import BaseEvent
from wagtail_ab_testing.models import AbTest
from wagtail_localize.models import (
    LocaleSynchronization,
    sync_trees_on_locale_sync_save,
)

from foundation_cms.legacy_apps.highlights.models import Highlight
from foundation_cms.legacy_apps.news.models import News
from foundation_cms.legacy_apps.wagtailcustomization.views.snippet_chooser import (
    DefaultLocaleSnippetChooserViewSet,
)
from foundation_cms.legacy_apps.wagtailpages import models as wagtailpages_models
from foundation_cms.legacy_apps.wagtailpages.pagemodels.buyersguide.homepage import (
    BuyersGuidePage,
)
from foundation_cms.legacy_apps.wagtailpages.pagemodels.buyersguide.products import (
    ProductPage,
)
from foundation_cms.legacy_apps.wagtailpages.pagemodels.campaigns import Callpower
from foundation_cms.legacy_apps.wagtailpages.utils import get_locale_from_request

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


@hooks.register("before_delete_page")
def delete_historical_ab_tests_before_page_deletion(request, page):
    """
    Fixes a bug where historical A/B tests prevent page deletion by removing them beforehand.
    Active A/B tests will still block deletion. For more info, see:
    https://github.com/wagtail-nest/wagtail-ab-testing/issues/90
    """
    # First, check if there is an active A/B test; if so, block deletion with an error message.
    if AbTest.objects.filter(page=page, status=AbTest.STATUS_RUNNING).exists():
        # Redirect to the parent page and display an error message in the CMS
        messages.error(request, "This page has an active A/B test and cannot be deleted.")
        return redirect("wagtailadmin_explore", page.get_parent().id)

    # If there are no active A/B tests, delete all historical A/B tests for the page
    # to prevent them from blocking the page deletion.
    historical_ab_tests = AbTest.objects.filter(page=page).exclude(status=AbTest.STATUS_RUNNING)
    if historical_ab_tests.exists():
        historical_ab_tests.delete()


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
        "icons/pni.svg",
        "icons/flask.svg",
        "icons/heart.svg",
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
    search_fields = (
        "name",
        "title",
    )
    ordering = ("name",)


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
    search_fields = ("name", "newsletter")
    ordering = ("name",)


class BlogViewSetGroup(SnippetViewSetGroup):
    items = (BlogPageTopicSnippetViewSet, BlogSignupSnippetViewSet)
    menu_icon = "bold"
    menu_label = "Blog"
    menu_name = "Blog"
    menu_order = 1400


register_snippet(BlogViewSetGroup)


class BuyersGuideProductCategorySnippetViewSet(SnippetViewSet):
    model = wagtailpages_models.BuyersGuideProductCategory
    icon = "list-ul"
    menu_order = 000
    menu_label = "Product Categories"
    menu_name = "Product Categories"
    list_display = (
        "name",
        "parent",
        "slug",
        BooleanColumn("featured"),
        BooleanColumn("hidden"),
        BooleanColumn("is_being_used"),
    )
    search_fields = ("name",)
    list_filter = (
        "featured",
        "hidden",
    )
    ordering = (
        "name",
        "parent",
    )


class BuyersGuideContentCategorySnippetViewSet(SnippetViewSet):
    model = wagtailpages_models.BuyersGuideContentCategory
    icon = "tag"
    menu_order = 100
    menu_label = "Content Categories"
    menu_name = "Content Categories"
    list_display = (
        "title",
        "slug",
    )
    search_fields = ("title",)
    ordering = ("title",)


class BuyersGuideUpdateSnippetViewSet(SnippetViewSet):
    model = wagtailpages_models.Update
    icon = "history"
    menu_order = 200
    menu_label = "Product Updates"
    menu_name = "Product Updates"
    list_display = (
        "title",
        "author",
        "linked_products",
        BooleanColumn("featured", label="Featured?"),
        "created_date",
    )
    search_fields = ("title",)
    list_filter = ("featured",)
    ordering = ("-created_date", "title", "source", "author")

    def get_queryset(self, request):
        """Return all updates with their related product pages pre-filtered by the request's locale."""
        language_code = request.GET.get("locale", "en")
        pages_in_request_locale = wagtailpages_models.ProductPage.objects.filter(
            locale__language_code=language_code,
            updates__update__isnull=False,
        )
        return wagtailpages_models.Update.objects.all().prefetch_related(
            Prefetch("product_pages__page", queryset=pages_in_request_locale)
        )


class BuyersGuideCTASnippetViewSet(SnippetViewSet):
    model = wagtailpages_models.BuyersGuideCallToAction
    icon = "link-external"
    menu_order = 300
    menu_label = "CTAs"
    menu_name = "CTAs"
    list_display = (
        "title",
        "link_label",
        "link_url",
    )
    search_fields = (
        "title",
        "link_label",
    )
    ordering = ("title",)


class BuyersGuideViewSetGroup(SnippetViewSetGroup):
    items = (
        BuyersGuideProductCategorySnippetViewSet,
        BuyersGuideContentCategorySnippetViewSet,
        BuyersGuideUpdateSnippetViewSet,
        BuyersGuideCTASnippetViewSet,
    )
    menu_icon = "pni"
    menu_label = "*PNI"
    menu_name = "*PNI"
    menu_order = 1500

    def get_submenu_items(self):
        menu_items = super().get_submenu_items()
        menu_items.append(SettingMenuItem(wagtailpages_models.BuyersGuideCategoryNav))
        return menu_items


register_snippet(BuyersGuideViewSetGroup)


class ResearchTopicsSnippetViewSet(SnippetViewSet):
    model = wagtailpages_models.ResearchTopic
    icon = "tag"
    menu_order = 000
    menu_label = "Topics"
    menu_name = "Topics"
    list_display = ("name", "slug")
    search_fields = ("name",)
    ordering = ("name",)


class ResearchRegionsSnippetViewSet(SnippetViewSet):
    model = wagtailpages_models.ResearchRegion
    icon = "globe"
    menu_order = 100
    menu_label = "Regions"
    menu_name = "Regions"
    list_display = ("name", "slug")
    search_fields = ("name",)
    ordering = ("name",)


class ResearchSetGroup(SnippetViewSetGroup):
    items = (ResearchTopicsSnippetViewSet, ResearchRegionsSnippetViewSet)
    menu_icon = "flask"
    menu_label = "Research Hub"
    menu_name = "Research Hub"
    menu_order = 1500


register_snippet(ResearchSetGroup)


class RCCContentTypeSnippetViewSet(SnippetViewSet):
    model = wagtailpages_models.RCCContentType
    icon = "clipboard-list"
    menu_order = 000
    menu_label = "Content Types"
    menu_name = "Content Types"
    list_display = ("name", "slug")
    search_fields = ("name",)
    ordering = ("name",)


class RCCCurricularAreaSnippetViewSet(SnippetViewSet):
    model = wagtailpages_models.RCCCurricularArea
    icon = "doc-full"
    menu_order = 100
    menu_label = "Curricular Areas"
    menu_name = "Curricular Areas"
    list_display = ("name", "slug")
    search_fields = ("name",)
    ordering = ("name",)


class RCCTopicsSnippetViewSet(SnippetViewSet):
    model = wagtailpages_models.RCCTopic
    icon = "tag"
    menu_order = 200
    menu_label = "Topics"
    menu_name = "Topics"
    list_display = ("name", "slug")
    search_fields = ("name",)
    ordering = ("name",)


class RCCSetGroup(SnippetViewSetGroup):
    items = (RCCContentTypeSnippetViewSet, RCCCurricularAreaSnippetViewSet, RCCTopicsSnippetViewSet)
    menu_icon = "desktop"
    menu_label = "RCC"
    menu_name = "RCC"
    menu_order = 1600


register_snippet(RCCSetGroup)


class PetitionsSnippetViewSet(SnippetViewSet):
    model = wagtailpages_models.Petition
    icon = "comment"
    menu_order = 1700
    menu_label = "Petitions"
    menu_name = "Petitions"
    add_to_admin_menu = True
    list_display = (
        "name",
        "newsletter",
        "campaign_id",
        BooleanColumn("show_country_field", label="Show country field?"),
        BooleanColumn("show_postal_code_field", label="Show postal code field?"),
        BooleanColumn("show_comment_field", label="Show comment field?"),
    )
    search_fields = (
        "name",
        "newsletter",
        "campaign_id",
    )
    list_filter = (
        "show_country_field",
        "show_postal_code_field",
        "show_comment_field",
    )
    ordering = (
        "name",
        "newsletter",
        "campaign_id",
    )


register_snippet(PetitionsSnippetViewSet)


class ProfilesSnippetViewSet(SnippetViewSet):
    model = wagtailpages_models.Profile
    icon = "user"
    menu_order = 1800
    menu_label = "Profiles"
    menu_name = "Profiles"
    add_to_admin_menu = True
    list_display = ("name", "tagline", "slug")
    search_fields = ("name",)
    ordering = ("name",)


register_snippet(ProfilesSnippetViewSet)


class CTASnippetViewSet(SnippetViewSet):
    model = wagtailpages_models.CTA
    icon = "link-external"
    menu_order = 1900
    menu_label = "CTAs"
    menu_name = "CTAs"
    add_to_admin_menu = True
    list_display = ("name", "header", "newsletter")
    search_fields = (
        "name",
        "newsletter",
    )
    ordering = ("name",)


register_snippet(CTASnippetViewSet)


class SignupSnippetViewSet(SnippetViewSet):
    model = wagtailpages_models.Signup
    icon = "newspaper"
    menu_order = 2000
    menu_label = "Signups"
    menu_name = "Signups"
    add_to_admin_menu = True
    list_display = (
        "name",
        "header",
        "newsletter",
        "campaign_id",
        BooleanColumn("ask_name", label="Ask for name?"),
    )
    search_fields = (
        "name",
        "newsletter",
        "campaign_id",
    )
    list_filter = ("ask_name",)
    ordering = ("name",)


register_snippet(SignupSnippetViewSet)


class AreasOfFocusViewSet(SnippetViewSet):
    model = wagtailpages_models.FocusArea
    icon = "view"
    menu_order = 000
    menu_label = "Areas of Focus"
    menu_name = "Areas of Focus"
    list_display = ("name", "interest_icon")
    search_fields = ("name",)
    ordering = ("name",)


class CallpowersViewSet(SnippetViewSet):
    model = Callpower
    icon = "chain-broken"
    menu_order = 100
    menu_label = "Callpowers"
    menu_name = "Callpowers"
    list_display = ("name", "header", "newsletter", "campaign_id", "call_button_label")
    search_fields = (
        "name",
        "newsletter",
        "campaign_id",
    )
    ordering = ("name",)


class HighlightSnippetViewSet(SnippetViewSet):
    model = Highlight
    icon = "date"
    menu_order = 200
    list_display = (
        "title",
        "link_label",
        "link_url",
    )
    search_fields = ("title", "link_label")
    ordering = ("title",)


class NewsSnippetViewSet(SnippetViewSet):
    model = News
    icon = "doc-full-inverse"
    menu_order = 300
    list_display = (
        "headline",
        "outlet",
        "author",
        "date",
        BooleanColumn("is_video", label="Is it video?"),
    )
    search_fields = (
        "headline",
        "outlet",
        "author",
    )
    list_filter = ("is_video",)
    ordering = ("-date", "outlet", "headline")


class PulseFiltersViewSet(SnippetViewSet):
    model = wagtailpages_models.PulseFilter
    icon = "cross"
    menu_order = 400
    menu_label = "Pulse Filters"
    menu_name = "Pulse Filters"
    list_display = ("name", "filter_key", "filter_key_label")
    search_fields = ("name",)
    list_filter = ("filter_key",)
    ordering = ("name",)


class ArchiveSetGroup(SnippetViewSetGroup):
    items = (AreasOfFocusViewSet, CallpowersViewSet, HighlightSnippetViewSet, NewsSnippetViewSet, PulseFiltersViewSet)
    menu_icon = "folder-open-1"
    menu_label = "Archived"
    menu_name = "Archived"
    menu_order = 2100


register_snippet(ArchiveSetGroup)

# --------------------------------------------------------------------------------------
# Register settings:
# --------------------------------------------------------------------------------------

register_setting(wagtailpages_models.BuyersGuideCategoryNav, icon="pni")


# --------------------------------------------------------------------------------------
# Default language choosers:
# --------------------------------------------------------------------------------------

# Customise choosers to only show models in the default language as options.
# We do not want editors to select the translations as localisation for these will be
# handled on the template instead.
# BE CAREFUL! Overriding the default chooser this way will take effect everywhere
# that a model is chosen!


@hooks.register("register_admin_viewset")
def register_donate_banner_chooser_viewset():
    return DefaultLocaleSnippetChooserViewSet(
        "wagtailsnippetchoosers_default_locale_product_category",
        model=wagtailpages_models.BuyersGuideProductCategory,
        url_prefix="wagtailpages/buyersguideproductcategory",
    )


# --------------------------------------------------------------------------------------
# Custom Wagtail A/B Testing Events:
# --------------------------------------------------------------------------------------


class DonateBannerLinkClick(BaseEvent):
    name = "Donate Banner Link Click"
    requires_page = False  # Set to False to create a "Global" event type that could be reached on any page


@hooks.register("register_ab_testing_event_types")
def register_donate_banner_link_click_event_type():
    return {
        "donate-banner-link-click": DonateBannerLinkClick,
    }
