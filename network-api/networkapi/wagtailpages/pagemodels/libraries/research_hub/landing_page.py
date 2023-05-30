from django.apps import apps
from django.db import models
from wagtail import models as wagtail_models
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail_localize.fields import SynchronizedField, TranslatableField

from networkapi.wagtailpages.pagemodels.base import BasePage


class ResearchLandingPage(BasePage):
    max_count = 1

    subpage_types = [
        "ResearchLibraryPage",
        "ResearchAuthorsIndexPage",
    ]

    template = "pages/research_hub/landing_page.html"

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
        InlinePanel("featured_topics", heading="Featured Topics"),
    ]

    translatable_fields = [
        TranslatableField("title"),
        SynchronizedField("banner_image"),
        TranslatableField("intro"),
        TranslatableField("featured_topics"),
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
        ResearchDetailPage = apps.get_model("wagtailpages", "ResearchDetailPage")
        research_detail_pages = ResearchDetailPage.objects.live().public()
        research_detail_pages = research_detail_pages.filter(locale=self.locale)
        research_detail_pages = research_detail_pages.order_by("-original_publication_date")
        research_detail_pages = research_detail_pages[:3]

        return research_detail_pages

    def get_library_page(self):
        ResearchLibraryPage = apps.get_model("wagtailpages", "ResearchLibraryPage")
        return ResearchLibraryPage.objects.filter(locale=self.locale).first()
