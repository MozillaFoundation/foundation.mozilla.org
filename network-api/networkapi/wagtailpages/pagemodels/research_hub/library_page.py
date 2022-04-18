import collections
from typing import Optional

from django.utils.translation import gettext_lazy as _
from wagtail.core import models as wagtail_models

from networkapi.wagtailpages import utils
from networkapi.wagtailpages.pagemodels import profiles as profile_models
from networkapi.wagtailpages.pagemodels.mixin import foundation_metadata
from networkapi.wagtailpages.pagemodels.research_hub import detail_page
from networkapi.wagtailpages.pagemodels.research_hub import taxonomies



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
        search_query = request.GET.get('search', '')
        sort_value = request.GET.get('sort', None)
        sort = self.SORT_CHOICES.get(sort_value, self.SORT_NEWEST_FIRST)
        filtered_author_ids = [
            int(author_id) for author_id in request.GET.getlist('author')
        ]
        filtered_topic_ids = [
            int(topic_id) for topic_id in request.GET.getlist('topic')
        ]

        context = super().get_context(request)
        context['search_query'] = search_query
        context['sort'] = sort
        context['author_options'] = self._get_author_options()
        context['filtered_author_ids'] = filtered_author_ids
        context['topic_options'] = self._get_topic_options()
        context['filtered_topic_ids'] = filtered_topic_ids
        context['research_detail_pages'] = self._get_research_detail_pages(
            search=search_query,
            sort=sort,
            author_profile_ids=filtered_author_ids,
            topic_ids=filtered_topic_ids,
        )
        return context

    def _get_author_options(self):
        author_options = profile_models.Profile.objects.filter_research_authors()
        return utils.localize_queryset(author_options)

    def _get_topic_options(self):
        topics = taxonomies.ResearchTopic.objects.all()
        return utils.localize_queryset(topics)

    def _get_research_detail_pages(
        self,
        *,
        search: str = '',
        sort: Optional[SortOption] = None,
        author_profile_ids: Optional[list[int]] = None,
        topic_ids: Optional[list[int]] = None,
    ):
        sort = sort or self.SORT_NEWEST_FIRST
        author_profile_ids = author_profile_ids or []
        topic_ids = topic_ids or []

        research_detail_pages = detail_page.ResearchDetailPage.objects.live()
        research_detail_pages = research_detail_pages.filter(
            locale=wagtail_models.Locale.get_active()
        )

        author_profiles = profile_models.Profile.objects.filter_research_authors()
        author_profiles = author_profiles.filter(id__in=author_profile_ids)
        for author_profile in author_profiles:
            # Synced but not translated pages are still associated with the default
            # locale's author profile. But, we want to show them when we are filtering
            # for the localized author profile. We use the fact that the localized and
            # default locale's author profile have the same `translation_key`.
            research_detail_pages = research_detail_pages.filter(
                research_authors__author_profile__translation_key=(
                    author_profile.translation_key
                )
            )

        topics = taxonomies.ResearchTopic.objects.filter(id__in=topic_ids)
        for topic in topics:
            research_detail_pages = research_detail_pages.filter(
                related_topics__research_topic__translation_key=topic.translation_key
            )

        research_detail_pages = research_detail_pages.order_by(sort.order_by_value)

        if search:
            research_detail_pages = research_detail_pages.search(
                search,
                order_by_relevance=False,  # To preserve original ordering
            )

        return research_detail_pages
