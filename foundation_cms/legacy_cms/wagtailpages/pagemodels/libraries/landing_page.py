from django.db import models
from wagtail import fields
from wagtail import models as wagtail_models
from wagtail.admin import panels
from wagtail_localize import fields as localize_fields

from legacy_cms.wagtailpages.pagemodels import customblocks
from legacy_cms.wagtailpages.pagemodels.base import BasePage
from legacy_cms.wagtailpages.pagemodels.libraries import constants


class BaseLandingPage(BasePage):
    max_count = 1

    parent_page_types = ["Homepage"]

    template = "pages/libraries/landing_page.html"

    intro = models.CharField(
        blank=True,
        max_length=250,
    )
    banner_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="Image that will render at the top of the page.",
    )
    body = fields.StreamField(
        block_types=(("about", customblocks.AboutBlock()),),
        null=True,
        blank=True,
        use_json_field=True,
    )
    aside_cta = fields.StreamField(
        block_types=(("cta", customblocks.CTAAsideBlock()),),
        null=True,
        blank=True,
        use_json_field=True,
        max_num=2,
    )

    content_panels = wagtail_models.Page.content_panels + [
        panels.FieldPanel("intro"),
        panels.FieldPanel("banner_image"),
        panels.FieldPanel("body"),
        panels.FieldPanel("aside_cta"),
    ]

    translatable_fields = [
        localize_fields.TranslatableField("title"),
        localize_fields.SynchronizedField("banner_image"),
        localize_fields.TranslatableField("intro"),
        localize_fields.TranslatableField("body"),
        localize_fields.TranslatableField("aside_cta"),
        # Promote tab fields
        localize_fields.SynchronizedField("slug"),
        localize_fields.TranslatableField("seo_title"),
        localize_fields.SynchronizedField("show_in_menus"),
        localize_fields.TranslatableField("search_description"),
        localize_fields.SynchronizedField("search_image"),
    ]

    @property
    def library_page(self):
        """Return the library page that this landing page is for."""
        raise NotImplementedError("Please implement this property in your subclass.")

    @property
    def detail_pages(self):
        """Return the detail pages that are children of this page."""
        raise NotImplementedError("Please implement this property in your subclass.")

    @property
    def latest_detail_pages(self):
        """Return the latest detail pages."""
        return self.detail_pages.order_by("-original_publication_date")[: constants.LATEST_ARTICLES_COUNT]

    class Meta:
        abstract = True
