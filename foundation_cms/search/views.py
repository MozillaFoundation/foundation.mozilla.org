from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count, Prefetch, prefetch_related_objects
from django.http import JsonResponse
from django.template.response import TemplateResponse
from wagtail.contrib.search_promotions.models import Query
from wagtail.models import Locale, Page
from wagtail.search.query import PlainText

from foundation_cms.base.models.abstract_base_page import PageTopic
from foundation_cms.campaigns.models.campaign_page import CampaignPage
from foundation_cms.search.models import SearchEvent
from foundation_cms.search.utils import (
    SECTION_SLUGS,
    get_search_backend_for_locale,
    normalize_content_type,
    normalize_sort,
    normalize_topic,
)
from foundation_cms.utils import get_default_locale, localize_queryset

# To enable logging of search queries for use with the "Promoted search results" module
# <https://docs.wagtail.org/en/stable/reference/contrib/searchpromotions.html>
# uncomment the following line and the lines indicated in the search function
# (after adding wagtail.contrib.search_promotions to INSTALLED_APPS):

# from wagtail.contrib.search_promotions.models import Query


def search(request):
    search_query = (request.GET.get("query") or "").strip()
    content_type = normalize_content_type(request.GET.get("content_type", "all"))
    sort = normalize_sort(request.GET.get("sort", "relevance"))
    selected_topic = normalize_topic(request.GET.get("topic"))
    related_topics = []
    page = request.GET.get("page", 1)
    total_search_results = 0
    current_locale = Locale.get_active()
    # Drawer count previews are internal requests and should not be logged as submitted searches.
    is_preview_request = request.headers.get("X-Search-Preview") == "true"
    is_initial_search_submit = "page" not in request.GET and not is_preview_request

    # Search
    if search_query:
        locale_code = current_locale.language_code
        base_queryset = Page.objects.live().filter(locale=current_locale)

        search_backend, backend_type = get_search_backend_for_locale(locale_code)
        backend_results = search_backend.search(search_query, base_queryset)

        # Extract IDs preserving backend's relevance order
        result_ids = [result.id for result in backend_results]

        # Remove duplicates while preserving order (in case the backend returns duplicates)
        result_ids = list(dict.fromkeys(result_ids))

        # Optional section filter by content_type slug
        section_slug = SECTION_SLUGS[content_type]
        if section_slug and result_ids:
            section_root = (
                Page.objects.live()
                .filter(locale=current_locale, slug=section_slug)
                .order_by("depth", "path", "id")
                .first()
            )

            if section_root:
                section_ids = set(
                    Page.objects.live()
                    .filter(id__in=result_ids)
                    .descendant_of(section_root, inclusive=False)
                    .values_list("id", flat=True)
                )
                result_ids = [pid for pid in result_ids if pid in section_ids]
            else:
                result_ids = []

        # Optional topic filter by tag slug (AFTER search backend, to avoid FilterFieldError on tag slug lookups)
        if selected_topic and result_ids:
            topic_ids = set(
                Page.objects.filter(
                    id__in=result_ids,
                    topic_relations__tag__slug=selected_topic,
                ).values_list("id", flat=True)
            )
            result_ids = [pid for pid in result_ids if pid in topic_ids]

        total_search_results = len(result_ids)

        # Build related topic facets from current query result set only
        search_results = []
        if result_ids:
            related_topics_qs = (
                Page.objects.filter(id__in=result_ids)
                .values("topic_relations__tag__slug", "topic_relations__tag__name")
                .exclude(topic_relations__tag__slug__isnull=True)
                .exclude(topic_relations__tag__name__isnull=True)
                .annotate(count=Count("id", distinct=True))
                .order_by("-count", "topic_relations__tag__name")
            )
            related_topics = [
                {
                    "slug": row["topic_relations__tag__slug"],
                    "name": row["topic_relations__tag__name"],
                    "count": row["count"],
                }
                for row in related_topics_qs[:20]
            ]

            # Create position mapping to restore relevance order later
            id_to_position = {pid: idx for idx, pid in enumerate(result_ids)}

            # Build optimized QuerySet with FK prefetch and specific() call
            search_results = list(
                Page.objects.filter(id__in=result_ids).select_related("search_image", "content_type").specific()
            )

            # Restore backend relevance order
            search_results.sort(key=lambda page: id_to_position.get(page.id, len(result_ids)))

        # Optional sorting by publication date
        if sort in ("newest", "oldest"):
            with_date = [p for p in search_results if p.first_published_at]
            without_date = [p for p in search_results if not p.first_published_at]

            with_date = sorted(
                with_date,
                key=lambda p: p.first_published_at,
                reverse=(sort == "newest"),
            )

            # Keep items without publication date at the end
            search_results = with_date + without_date

        # Log only on initial submission, not on pagination clicks
        if is_initial_search_submit:
            SearchEvent.objects.create(
                query_string=search_query.lower(),
                language_code=current_locale.language_code,
                results_count=total_search_results,
            )

            query = Query.get(search_query)
            query.add_hit()

    else:
        search_results = Page.objects.none()

    # Pagination
    paginator = Paginator(search_results, 10)
    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)

    prefetch_related_objects(
        search_results.object_list,
        Prefetch(
            "topic_relations",
            queryset=PageTopic.objects.select_related("tag").order_by("id"),
            to_attr="search_topic_relations",
        ),
    )

    # Keep contributing pages when there are no results
    keep_contributing_pages = []
    if search_query and not search_results.object_list:
        # TODO: Temporary hardcoded page IDs via env var until we have enough pages to auto pull.
        #       Revert to keep_contributing_pages = get_keep_contributing_pages() when ready.
        hardcoded_pages = Page.objects.live().filter(id__in=settings.TEMP_SEARCH_RELATED_CONTENT_PAGE_IDS)
        localized_pages = localize_queryset(hardcoded_pages, preserve_order=True)
        keep_contributing_pages = list(localized_pages.specific()[:2])

    return TemplateResponse(
        request,
        "search/search_page.html",
        {
            "search_query": search_query,
            "search_results": search_results,
            "total_search_results": total_search_results,
            "keep_contributing_pages": keep_contributing_pages,
            "current_locale": current_locale.language_code,
            "sort": sort,
            "content_type": content_type,
            "selected_topic": selected_topic,
            "related_topics": related_topics,
            "autocomplete_min_chars": settings.SEARCH_AUTOCOMPLETE_MIN_CHARS,
        },
    )


def get_keep_contributing_pages():
    """
    Get the two latest CampaignPages in their localized versions.
    Follows the same pattern as CampaignPage.get_fallback_latest_campaigns().
    """
    default_locale, _ = get_default_locale()

    # Get recent pages in the default language
    recent_pages = CampaignPage.objects.live().public().filter(locale=default_locale).order_by("-first_published_at")

    localized_pages = localize_queryset(
        recent_pages,
        preserve_order=True,
    )

    return list(localized_pages.specific()[:2])


def search_autocomplete(request):
    min_chars = settings.SEARCH_AUTOCOMPLETE_MIN_CHARS
    search_query = request.GET.get("query", "").strip()
    if search_query and len(search_query) >= min_chars:
        results = (
            Page.objects.live()
            .filter(locale=Locale.get_active())
            .autocomplete(PlainText(search_query), fields=["title"], operator="or")[:5]
        )  # Limit to 5 suggestions
        return JsonResponse({"results": [{"title": page.title, "url": page.url} for page in results]})
    return JsonResponse({"results": []})
