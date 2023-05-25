from django.apps import apps
from django.db import models
from wagtail import models as wagtail_models
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail_localize.fields import SynchronizedField, TranslatableField

from networkapi.wagtailpages.pagemodels.base import BasePage


class RCCLandingPage(BasePage):
    max_count = 1

    subpage_types = [
        "RCCLibraryPage",
        "RCCAuthorsIndexPage",
    ]

    template = "pages/rcc/landing_page.html"

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
        FieldPanel("intro"),
        FieldPanel("banner_image"),
        InlinePanel("featured_content_types", heading="Featured content types"),
    ]

    translatable_fields = [
        TranslatableField("title"),
        SynchronizedField("banner_image"),
        TranslatableField("intro"),
        TranslatableField("featured_content_types"),
        # Promote tab fields
        SynchronizedField("slug"),
        TranslatableField("seo_title"),
        SynchronizedField("show_in_menus"),
        TranslatableField("search_description"),
        SynchronizedField("search_image"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context["library_page"] = self.get_library_page()
        context["latest_research_detail_pages"] = self.get_latest_research_pages()
        return context

    def get_latest_research_pages(self):
        RCCDetailPage = apps.get_model("wagtailpages", "RCCDetailPage")
        rcc_detail_pages = RCCDetailPage.objects.live().public()
        rcc_detail_pages = rcc_detail_pages.filter(locale=self.locale)
        rcc_detail_pages = rcc_detail_pages.order_by("-original_publication_date")
        rcc_detail_pages = rcc_detail_pages[:3]

        return rcc_detail_pages

    def get_library_page(self):
        RCCLibraryPage = apps.get_model("wagtailpages", "RCCLibraryPage")
        return RCCLibraryPage.objects.filter(locale=self.locale).first()
