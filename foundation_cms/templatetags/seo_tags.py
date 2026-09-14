from django import template
from django.utils.translation import get_language
from wagtail.models import Locale

register = template.Library()


@register.simple_tag(takes_context=True)
def content_language(context, page=None):
    """The language of what's actually rendered, not the URL locale prefix (wrong for aliases)."""
    page = page or context.get("page")
    if page is None:
        return get_language()

    source_page = page.alias_of if page.alias_of_id else page
    return source_page.locale.language_code


@register.inclusion_tag("patterns/components/_seo_links.html", takes_context=True)
def seo_links(context, page=None):
    page = page or context.get("page")
    request = context.get("request")
    if page is None or request is None:
        return {"canonical_url": None, "hreflang_links": []}

    site_url = f"{request.scheme}://{request.get_host()}"

    if page.alias_of_id:
        return {
            "canonical_url": site_url + page.alias_of.get_url(request=request),
            "hreflang_links": [],
        }

    canonical_url = site_url + page.get_url(request=request)
    translations = page.get_translations().live().public().filter(alias_of__isnull=True).select_related("locale")

    hreflang_links = []
    if translations:
        default_locale = Locale.get_default()
        hreflang_links = [{"hreflang": page.locale.language_code, "url": canonical_url, "locale_id": page.locale_id}]
        for translation in translations:
            hreflang_links.append(
                {
                    "hreflang": translation.locale.language_code,
                    "url": site_url + translation.get_url(request=request),
                    "locale_id": translation.locale_id,
                }
            )

        default_link = next(
            (link for link in hreflang_links if link["locale_id"] == default_locale.id),
            hreflang_links[0],
        )
        hreflang_links.append({"hreflang": "x-default", "url": default_link["url"]})

    return {
        "canonical_url": canonical_url,
        "hreflang_links": hreflang_links,
    }
