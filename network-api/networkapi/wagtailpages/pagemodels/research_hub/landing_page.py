from django.apps import apps
from wagtail.core import models as wagtail_models
from django.db import models


from networkapi.wagtailpages.pagemodels.mixin import foundation_metadata
from wagtail.admin.edit_handlers import (
    FieldPanel, InlinePanel
)


class ResearchLandingPage(foundation_metadata.FoundationMetadataPageMixin, wagtail_models.Page):
    max_count = 1
    subpage_types = [
        'ResearchLibraryPage',
        'ResearchAuthorsIndexPage',
    ]

    intro = models.CharField(
        blank=True,
        max_length=250,
    )

    content_panels = wagtail_models.Page.content_panels + [
        FieldPanel('intro'),
        InlinePanel('featured_topics', heading="Featured Topics"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        ResearchLibraryPage = apps.get_model("wagtailpages", "ResearchLibraryPage")
        context['library_page'] = ResearchLibraryPage.objects.first()
        context['latest_research_detail_pages'] = self.get_latest_research_pages
        return context

    def get_latest_research_pages(self):
        active_locale = wagtail_models.Locale.get_active()

        ResearchDetailPage = apps.get_model('wagtailpages', 'ResearchDetailPage')
        research_detail_pages = ResearchDetailPage.objects.live()
        research_detail_pages = research_detail_pages.filter(locale=active_locale)
        research_detail_pages = research_detail_pages.order_by('-original_publication_date')
        research_detail_pages = research_detail_pages[:3]

        return research_detail_pages
