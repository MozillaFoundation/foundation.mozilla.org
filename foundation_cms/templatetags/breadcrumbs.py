from django import template

register = template.Library()


def _localize_page(p, request):
    """
    Return the page localized to the active language if possible.
    Wagtail i18n provides `.localized` on translatable models.
    """
    try:
        return p.localized
    except Exception:
        return p


@register.inclusion_tag("patterns/components/breadcrumbs.html", takes_context=True)
def breadcrumbs(context, page=None):
    request = context.get("request")
    page = page or context.get("page")
    if not page or not request:
        return {"breadcrumbs": [], "mobile_breadcrumbs": [], "mobile_has_more": False}

    # Ancestors inclusive so the current page is included at the end.
    # Exclude Wagtail root (depth=1).
    ancestors = page.get_ancestors(inclusive=True).filter(depth__gt=2)

    trail = [_localize_page(p, request) for p in ancestors]

    # Desktop: full trail
    breadcrumbs_list = trail

    # Mobile: only 1 parent ancestor + current page.
    # If there are more ancestors above the nearest parent, show a leading "/".
    if len(trail) >= 2:
        mobile_breadcrumbs = trail[-2:]
        mobile_show_leading_slash = len(trail) > 2
    else:
        mobile_breadcrumbs = trail
        mobile_show_leading_slash = False

    # Set false if no non-homepage parent ancestor
    if len(breadcrumbs_list) <= 1:
        breadcrumbs_list = False

    return {
        "breadcrumbs": breadcrumbs_list,
        "mobile_breadcrumbs": mobile_breadcrumbs,
        "mobile_show_leading_slash": mobile_show_leading_slash,
        "request": request,
    }
