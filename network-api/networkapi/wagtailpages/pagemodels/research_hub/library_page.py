from django.apps import apps
from wagtail.core import models as wagtail_models

from networkapi.wagtailpages.pagemodels.mixin import foundation_metadata


class ResearchLibraryPage(foundation_metadata.FoundationMetadataPageMixin, wagtail_models.Page):
    max_count = 1
    parent_page_types = ['ResearchLandingPage']
    subpage_types = ['ResearchDetailPage']

    SORT_NEWEST_FIRST = '-original_publication_date'

    def get_context(self, request):
        context = super().get_context(request)

        search_query = request.GET.get('search', '')
        context['search_query'] = search_query

        context['research_detail_pages'] = self.get_research_detail_pages(
            search=search_query
        )
        return context

    def get_research_detail_pages(self, *, search='', sort=None):
        ResearchDetailPage = apps.get_model('wagtailpages', 'ResearchDetailPage')
        active_locale = wagtail_models.Locale.get_active()

        research_detail_pages = ResearchDetailPage.objects.live()
        research_detail_pages = research_detail_pages.filter(locale=active_locale)
        research_detail_pages = research_detail_pages.order_by(self.SORT_NEWEST_FIRST)
        if search:
            research_detail_pages = research_detail_pages.search(search)

        return research_detail_pages
