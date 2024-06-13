from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtail_localize.fields import SynchronizedField, TranslatableField

from ..utils import get_page_tree_information
from .base import BasePage
from .customblocks.base_fields import base_fields


class ModularPage(BasePage):
    """
    This base class offers universal component picking.
    Note: this is a legacy class, see
    https://github.com/mozilla/foundation.mozilla.org/issues/5071#issuecomment-675720719
    """

    header = models.CharField(max_length=250, blank=True)

    narrowed_page_content = models.BooleanField(
        default=False,
        help_text="For text-heavy pages, turn this on to reduce the overall width of the content on the page.",
    )

    body = StreamField(base_fields, use_json_field=True)

    settings_panels = Page.settings_panels + [
        MultiFieldPanel(
            [
                FieldPanel("narrowed_page_content"),
            ],
            classname="collapsible",
        ),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("header"),
        FieldPanel("body"),
    ]

    translatable_fields = [
        # Promote tab fields
        SynchronizedField("slug"),
        TranslatableField("seo_title"),
        SynchronizedField("show_in_menus"),
        TranslatableField("search_description"),
        SynchronizedField("search_image"),
        # Content tab fields
        TranslatableField("header"),
        SynchronizedField("narrowed_page_content"),
    ]

    show_in_menus_default = True


class MiniSiteNameSpace(ModularPage):
    subpage_types = [
        "BlogPage",
        "CampaignPage",
        "BanneredCampaignPage",
        "OpportunityPage",
        "YoutubeRegretsPage",
        "ArticlePage",
    ]

    """
    This is basically an abstract page type for setting up
    minisite namespaces such as "campaign", "opportunity", etc.
    """

    def get_context(self, request):
        """
        Extend the context so that mini-site pages know what kind of tree
        they live in, and what some of their local aspects are:
        """
        context = super().get_context(request)
        updated = get_page_tree_information(self, context)
        updated["mini_site_title"] = updated["root"].title
        return updated
