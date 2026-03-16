from django import template
from wagtail import models as wagtail_models

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


@register.inclusion_tag("patterns/components/breadcrumb_nav.html", takes_context=True)
def breadcrumb_nav(context, page=None):
    request = context.get("request")
    page = page or context.get("page")
    if not page or not request:
        return {"breadcrumbs": [], "mobile_breadcrumbs": [], "mobile_show_leading_slash": False}

    site = wagtail_models.Site.find_for_request(request)
    site_root = site.root_page if site else None

    ancestors = page.get_ancestors(inclusive=True).filter(depth__gt=2)
    if site_root:
        ancestors = ancestors.exclude(translation_key=site_root.translation_key)

    trail = [_localize_page(p) for p in ancestors]

    # Desktop: full trail
    breadcrumbs_list = trail if len(trail) > 1 else False

    # Mobile: only 1 parent ancestor + current page.
    # If there are more ancestors above the nearest parent, show a leading "/".
    if len(trail) >= 2:
        mobile_breadcrumbs = trail[-2:]
        mobile_show_leading_slash = len(trail) > 2
    else:
        mobile_breadcrumbs = trail
        mobile_show_leading_slash = False

    return {
        "breadcrumbs": breadcrumbs_list,
        "mobile_breadcrumbs": mobile_breadcrumbs,
        "mobile_show_leading_slash": mobile_show_leading_slash,
        "request": request,
    }
