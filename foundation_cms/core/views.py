from django.shortcuts import render
from wagtail.models import Page, Locale


def listing_page(request):
    # Get the tag from the query parameters
    tag = request.GET.get('tag')

    # Get the current locale
    locale = Locale.get_active()

    # Get all pages for the current locale
    pages = Page.objects.live().public().filter(locale=locale)

    # Filter by tag if provided
    if tag:
        pages = pages.filter(base_tagged_items__tag__slug=tag)
    else:
        pages = pages.all()

    context = {
        'pages': pages,
        'active_tag': tag if tag else 'Latest Posts'
    }

    return render(request, "patterns/pages/core/listing_page.html", context)
