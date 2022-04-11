import collections

from django.apps import apps
from django.utils.translation import gettext_lazy as _
from wagtail.core import models as wagtail_models

from networkapi.wagtailpages.pagemodels.mixin import foundation_metadata


# We don't want to expose the actual database column value that we use for sorting.
# Therefore, we need a separate value that is used in the form and url.
SortOption = collections.namedtuple(
    'SortOption',
    ['label', 'value', 'order_by_value']
)


class ResearchLibraryPage(foundation_metadata.FoundationMetadataPageMixin, wagtail_models.Page):
    max_count = 1
    parent_page_types = ['ResearchLandingPage']
    subpage_types = ['ResearchDetailPage']

    SORT_NEWEST_FIRST = SortOption(
        label=_('Newest first'),
        value='newest-first',
        order_by_value='-original_publication_date',
    )
    SORT_OLDEST_FIRST = SortOption(
        label=_('Oldest first'),
        value='oldest-first',
        order_by_value='original_publication_date',
    )
    SORT_ALPHABETICAL = SortOption(
        label=_('Alphabetical (A-Z)'),
        value='alphabetical',
        order_by_value='title',
    )
    SORT_ALPHABETICAL_REVERSED = SortOption(
        label=_('Alphabetical (Z-A)'),
        value='alphabetical-reversed',
        order_by_value='-title',
    )
    SORT_CHOICES = {
        SORT_NEWEST_FIRST.value: SORT_NEWEST_FIRST,
        SORT_OLDEST_FIRST.value: SORT_OLDEST_FIRST,
        SORT_ALPHABETICAL.value: SORT_ALPHABETICAL,
        SORT_ALPHABETICAL_REVERSED.value: SORT_ALPHABETICAL_REVERSED,
    }

    def get_context(self, request):
        context = super().get_context(request)

        search_query = request.GET.get('search', '')
        context['search_query'] = search_query

        sort_value = request.GET.get('sort', None)
        sort = self.SORT_CHOICES.get(sort_value, self.SORT_NEWEST_FIRST)
        context['sort'] = sort

        context['research_detail_pages'] = self.get_research_detail_pages(
            search=search_query,
            sort=sort,
        )
        return context

    def get_research_detail_pages(self, *, search='', sort=None):
        sort = sort or self.SORT_NEWEST_FIRST

        active_locale = wagtail_models.Locale.get_active()

        ResearchDetailPage = apps.get_model('wagtailpages', 'ResearchDetailPage')
        research_detail_pages = ResearchDetailPage.objects.live()
        research_detail_pages = research_detail_pages.filter(locale=active_locale)
        research_detail_pages = research_detail_pages.order_by(sort.order_by_value)
        if search:
            research_detail_pages = research_detail_pages.search(
                search,
                order_by_relevance=False,  # To preserve original ordering
            )

        return research_detail_pages
