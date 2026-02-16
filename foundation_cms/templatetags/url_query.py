from __future__ import annotations

from django import template
from django.http import QueryDict
from django.urls import reverse

register = template.Library()


@register.simple_tag(takes_context=True)
def url_with_query(context, viewname: str, **overrides) -> str:
    """Build a URL (via `reverse`) and merge/override query params.

    Uses `request.GET` as the base when available.

    Template usage:
        {% url_with_query 'search' query=search_query page=2 %}
        {% url_with_query 'search' page=page_obj.next_page_number as next_url %}
    """

    base_url = reverse(viewname)

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
