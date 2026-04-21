from __future__ import annotations

from django import template
from django.http import QueryDict
from django.urls import reverse

register = template.Library()


@register.simple_tag(takes_context=True)
def url_with_query(context, viewname: str = "", **overrides) -> str:
    """Build a URL and merge/override query params.

    Pass either a ``viewname`` (resolved via ``reverse``) or a ``base_url``
    kwarg for pages that have no registered URL name (e.g. Wagtail pages).
    Uses ``request.GET`` as the base query string when available.

    Template usage:
        {% url_with_query 'search' query=search_query page=2 %}
        {% url_with_query base_url=request.path page=page_obj.next_page_number as next_url %}
    """

    base_url = overrides.pop("base_url", None)
    if viewname:
        base_url = reverse(viewname)
    elif not base_url:
        raise ValueError("url_with_query requires either a viewname or base_url")

    request = context.get("request")
    query_params = request.GET.copy() if request is not None else QueryDict("", mutable=True)

    for key, value in overrides.items():
        if value is None or value == "":
            query_params.pop(key, None)
            continue

        if isinstance(value, (list, tuple)):
            query_params.setlist(key, [str(item) for item in value])
        else:
            query_params[key] = str(value)

    encoded = query_params.urlencode()
    if not encoded:
        return base_url

    return f"{base_url}?{encoded}"
