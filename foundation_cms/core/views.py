from django.shortcuts import render
from foundation_cms.base.models import AbstractArticlePage


def listing_page(request):
    # Get the tag from the query parameters
    tag = request.GET.get('tag')

    # Get all pages
    pages = AbstractArticlePage.objects.live().public()

    # Filter by tag if provided
    if tag:
        articles = pages.filter(base_tagged_items__tag__slug=tag)
    else:
        articles = pages.all()

    context = {
        'articles': articles,
        'active_tag': tag if tag else 'Latest Posts'
    }

    return render(request, "patterns/pages/core/listing_page.html", context)
