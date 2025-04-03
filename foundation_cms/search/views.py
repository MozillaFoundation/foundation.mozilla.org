from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import JsonResponse
from django.template.response import TemplateResponse
from wagtail.models import Locale, Page
from wagtail.search.query import PlainText

# To enable logging of search queries for use with the "Promoted search results" module
# <https://docs.wagtail.org/en/stable/reference/contrib/searchpromotions.html>
# uncomment the following line and the lines indicated in the search function
# (after adding wagtail.contrib.search_promotions to INSTALLED_APPS):

# from wagtail.contrib.search_promotions.models import Query


def search(request):
    search_query = request.GET.get("query", None)
    page = request.GET.get("page", 1)

    # Search
    if search_query:
        search_results = Page.objects.live().filter(locale=Locale.get_active()).search(search_query)

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

    return TemplateResponse(
        request,
        "search/search.html",
        {
            "search_query": search_query,
            "search_results": search_results,
        },
    )


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
