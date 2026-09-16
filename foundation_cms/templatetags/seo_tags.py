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


def _absolute_url(site_url, path):
    if not site_url or not path:
        return None
    return site_url + path


def _routed_suffix(page_path, request):
    """Extra path beyond page_path, e.g. a RoutablePageMixin sub-route like /topics/privacy/."""
    if page_path and request.path.startswith(page_path):
        return request.path[len(page_path) :]
    return ""


@register.inclusion_tag("patterns/components/_seo_links.html", takes_context=True)
def seo_links(context, page=None):
    page = page or context.get("page")
    request = context.get("request")
    if page is None or request is None:
        return {"canonical_url": None, "hreflang_links": []}

    site_url = context.get("CANONICAL_SITE_URL")

    if page.alias_of_id:
        canonical_url = _absolute_url(site_url, page.alias_of.get_url(request=request))
        return {
            "canonical_url": canonical_url,
            "hreflang_links": [],
        }

    page_path = page.get_url(request=request)
    suffix = _routed_suffix(page_path, request)
    canonical_url = _absolute_url(site_url, page_path + suffix if page_path else None)
    translations = list(page.get_translations().live().public().filter(alias_of__isnull=True).select_related("locale"))

    hreflang_links = []
    if translations:
        try:
            default_locale = Locale.get_default()
        except Locale.DoesNotExist:
            default_locale = None

        default_url = None
        if canonical_url:
            hreflang_links.append({"hreflang": page.locale.language_code, "url": canonical_url})
            if default_locale and page.locale_id == default_locale.id:
                default_url = canonical_url

        for translation in translations:
            translation_path = translation.get_url(request=request)
            url = _absolute_url(site_url, translation_path + suffix if translation_path else None)
            if not url:
                continue
            hreflang_links.append({"hreflang": translation.locale.language_code, "url": url})
            if default_locale and translation.locale_id == default_locale.id:
                default_url = url

        if hreflang_links:
            hreflang_links.append({"hreflang": "x-default", "url": default_url or hreflang_links[0]["url"]})

    return {
        "canonical_url": canonical_url,
        "hreflang_links": hreflang_links,
    }
