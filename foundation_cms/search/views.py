from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import JsonResponse
from django.template.response import TemplateResponse
from wagtail.models import Locale, Page
from wagtail.search.query import PlainText

from foundation_cms.campaigns.models.campaign_page import CampaignPage
from foundation_cms.utils import get_default_locale, localize_queryset
from foundation_cms.search.utils import (
    get_search_backend_for_locale,
    should_use_locale_backend,
)

# To enable logging of search queries for use with the "Promoted search results" module
# <https://docs.wagtail.org/en/stable/reference/contrib/searchpromotions.html>
# uncomment the following line and the lines indicated in the search function
# (after adding wagtail.contrib.search_promotions to INSTALLED_APPS):

# from wagtail.contrib.search_promotions.models import Query


def search(request):
    search_query = request.GET.get("query", None)
    page = request.GET.get("page", 1)
    total_search_results = 0

    # Search
    if search_query:
        # Get current locale and base queryset
        current_locale = Locale.get_active()
        locale_code = current_locale.language_code
        base_queryset = Page.objects.live().filter(locale=current_locale)

        # Use appropriate search backend
        if should_use_locale_backend(locale_code):
            search_backend, backend_type = get_search_backend_for_locale(locale_code)
            search_results = search_backend.search(search_query, base_queryset)
        else:
            # Use default search with 'simple' configuration for unsupported languages
            search_results = base_queryset.search(search_query)

        total_search_results = search_results.count()

        # To log this query for use with the "Promoted search results" module:

        # query = Query.get(search_query)
        # query.add_hit()

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

    # Keep contributing pages when there are no results
    keep_contributing_pages = []
    if search_query and not search_results.object_list:
        keep_contributing_pages = get_keep_contributing_pages()

    return TemplateResponse(
        request,
        "search/search.html",
        {
            "search_query": search_query,
            "search_results": search_results,
            "total_search_results": total_search_results,
            "keep_contributing_pages": keep_contributing_pages,
            "current_locale": current_locale.language_code,
        },
    )


def get_keep_contributing_pages():
    """
    Get the two latest CampaignPages in their localized versions.
    Follows the same pattern as CampaignPage.get_fallback_latest_campaigns().
    """
    (default_locale, _) = get_default_locale()

    # Get recent pages in the default language
    recent_pages = CampaignPage.objects.live().public().filter(locale=default_locale).order_by("-first_published_at")

    localized_pages = localize_queryset(
        recent_pages,
        preserve_order=True,
    )

    return list(localized_pages.specific()[:2])


def search_autocomplete(request):
    search_query = request.GET.get("query", "").strip()
    if search_query:
        results = (
            Page.objects.live()
            .filter(locale=Locale.get_active())
            .autocomplete(PlainText(search_query), fields=["title"], operator="or")[:5]
        )  # Limit to 5 suggestions
        return JsonResponse({"results": [{"title": page.title, "url": page.url} for page in results]})
    return JsonResponse({"results": []})
