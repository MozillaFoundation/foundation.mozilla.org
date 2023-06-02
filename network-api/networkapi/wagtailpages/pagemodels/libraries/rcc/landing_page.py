from django.apps import apps
from django.db import models
from wagtail import models as wagtail_models
from wagtail.admin import panels
from wagtail_localize import fields as localize_fields

from networkapi.wagtailpages.pagemodels.base import BasePage


class RCCLandingPage(BasePage):
    max_count = 1

    subpage_types = [
        "RCCLibraryPage",
        "RCCAuthorsIndexPage",
    ]

    template = "pages/libraries/rcc/landing_page.html"

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

    content_panels = wagtail_models.Page.content_panels + [
        panels.FieldPanel("intro"),
        panels.FieldPanel("banner_image"),
        panels.InlinePanel("featured_content_types", heading="Featured content types"),
    ]

    translatable_fields = [
        localize_fields.TranslatableField("title"),
        localize_fields.SynchronizedField("banner_image"),
        localize_fields.TranslatableField("intro"),
        localize_fields.TranslatableField("featured_content_types"),
        # Promote tab fields
        localize_fields.SynchronizedField("slug"),
        localize_fields.TranslatableField("seo_title"),
        localize_fields.SynchronizedField("show_in_menus"),
        localize_fields.TranslatableField("search_description"),
        localize_fields.SynchronizedField("search_image"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context["library_page"] = self.get_library_page()
        context["latest_rcc_detail_pages"] = self.get_latest_rcc_pages()
        return context

    def get_latest_rcc_pages(self):
        RCCDetailPage = apps.get_model("wagtailpages", "RCCDetailPage")
        rcc_detail_pages = RCCDetailPage.objects.live().public()
        rcc_detail_pages = rcc_detail_pages.filter(locale=self.locale)
        rcc_detail_pages = rcc_detail_pages.order_by("-original_publication_date")
        rcc_detail_pages = rcc_detail_pages[:3]

        return rcc_detail_pages

    def get_library_page(self):
        RCCLibraryPage = apps.get_model("wagtailpages", "RCCLibraryPage")
        return RCCLibraryPage.objects.filter(locale=self.locale).first()
