from django.apps import apps
from wagtail.core import models as wagtail_models

from networkapi.wagtailpages.pagemodels.mixin import foundation_metadata


class ResearchLibraryPage(foundation_metadata.FoundationMetadataPageMixin, wagtail_models.Page):
    max_count = 1
    parent_page_types = ['ResearchLandingPage']
    subpage_types = ['ResearchDetailPage']

    SORT_NEWEST_FIRST = '-original_publication_date'
    SORT_OLDEST_FIRST = 'original_publication_date'
    SORT_ALPHABETICAL = 'title'
    SORT_ALPHABETICAL_REVERSED = '-title'

    def get_context(self, request):
        context = super().get_context(request)

        search_query = request.GET.get('search', '')
        context['search_query'] = search_query

        context['research_detail_pages'] = self.get_research_detail_pages(
            search=search_query
        )
        return context

    def get_research_detail_pages(self, *, search='', sort=None):
        sort = sort or self.SORT_NEWEST_FIRST

        active_locale = wagtail_models.Locale.get_active()

        ResearchDetailPage = apps.get_model('wagtailpages', 'ResearchDetailPage')
        research_detail_pages = ResearchDetailPage.objects.live()
        research_detail_pages = research_detail_pages.filter(locale=active_locale)
        research_detail_pages = research_detail_pages.order_by(sort)
        if search:
            research_detail_pages = research_detail_pages.search(
                search,
                order_by_relevance=False, # To preseve original ordering
            )

        return research_detail_pages
