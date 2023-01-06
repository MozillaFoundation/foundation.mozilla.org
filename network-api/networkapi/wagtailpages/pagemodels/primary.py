from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, StreamFieldPanel
from wagtail.fields import StreamField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.models import Page
from wagtail_localize.fields import SynchronizedField, TranslatableField

from ..utils import get_page_tree_information, set_main_site_nav_information
from .customblocks.base_fields import base_fields
from .mixin.foundation_banner_inheritance import FoundationBannerInheritanceMixin
from .mixin.foundation_metadata import FoundationMetadataPageMixin


class PrimaryPage(FoundationMetadataPageMixin, FoundationBannerInheritanceMixin, Page):
    """
    Basically a straight copy of modular page, but with
    restrictions on what can live 'under it'.

    Ideally this is just PrimaryPage(ModularPage) but
    setting that up as a migration seems to be causing
    problems.
    """

    header = models.CharField(max_length=250, blank=True)

    banner = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="primary_banner",
        verbose_name="Hero Image",
        help_text="Choose an image that's bigger than 4032px x 1152px with aspect ratio 3.5:1",
    )

    intro = models.CharField(
        max_length=350,
        blank=True,
        help_text="Intro paragraph to show in hero cutout box",
    )

    narrowed_page_content = models.BooleanField(
        default=False,
        help_text="For text-heavy pages, turn this on to reduce the overall width of the content on the page.",
    )

    zen_nav = models.BooleanField(
        default=False,
        help_text="For secondary nav pages, use this to collapse the primary nav under a toggle hamburger.",
    )

    body = StreamField(base_fields, use_json_field=True)

    settings_panels = Page.settings_panels + [
        MultiFieldPanel(
            [
                FieldPanel("narrowed_page_content"),
            ],
            classname="collapsible",
        ),
        MultiFieldPanel(
            [
                FieldPanel("zen_nav"),
            ],
            classname="collapsible",
        ),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("header"),
        ImageChooserPanel("banner"),
        FieldPanel("intro"),
        StreamFieldPanel("body"),
    ]

    translatable_fields = [
        # Promote tab fields
        SynchronizedField("slug"),
        TranslatableField("seo_title"),
        SynchronizedField("show_in_menus"),
        TranslatableField("search_description"),
        SynchronizedField("search_image"),
        # Content tab fields
        TranslatableField("title"),
        TranslatableField("header"),
        SynchronizedField("banner"),
        TranslatableField("intro"),
        TranslatableField("body"),
        SynchronizedField("narrowed_page_content"),
        SynchronizedField("zen_nav"),
    ]

    subpage_types = [
        "PrimaryPage",
        "RedirectingPage",
        "BanneredCampaignPage",
        "OpportunityPage",
        "ArticlePage",
    ]

    show_in_menus_default = True

    def get_context(self, request):
        context = super().get_context(request)
        context = set_main_site_nav_information(self, context, "Homepage")
        context = get_page_tree_information(self, context)
        return context
