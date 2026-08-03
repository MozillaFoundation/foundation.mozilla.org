from urllib.parse import urlsplit

from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag(takes_context=True)
def translated_menu(context, menu):
    """
    Return a translated version of `menu` for the current page locale when available.
    Falls back to the original menu.
    """
    if not menu:
        return None

    page = context.get("page")
    locale = getattr(page, "locale", None)
    if not locale:
        return menu

    if getattr(menu, "locale_id", None) == locale.id:
        return menu

    translated = menu.get_translation_or_none(locale)
    return translated or menu


def _supported_locale_codes():
    return {code.strip("/") for code, _name in settings.LANGUAGES}


def _normalized_path(url, strip_locale=False):
    try:
        path = urlsplit(url or "").path
    except (TypeError, ValueError):
        return None

    if not path:
        return None
    if path == "/":
        return path

    normalized = f"/{path.strip('/')}"

    if strip_locale:
        parts = normalized.strip("/").split("/")
        if parts and parts[0] in _supported_locale_codes():
            parts = parts[1:]
            normalized = f"/{'/'.join(parts)}" if parts else "/"

    return normalized


def _link_is_active(current_path, link_url, is_external=False, strip_locale=False):
    if is_external:
        return False

    current = _normalized_path(current_path, strip_locale=strip_locale)
    target = _normalized_path(link_url, strip_locale=strip_locale)
    if not current or not target:
        return False
    if target == "/":
        return current == target
    return current == target or current.startswith(f"{target}/")


def _internal_link_url(request, link):
    if not link or link.is_external:
        return None

    url = link.get_url_for_request(request)
    try:
        parsed_url = urlsplit(url or "")
    except (TypeError, ValueError):
        return None

    if parsed_url.scheme or parsed_url.netloc:
        return None

    return url


@register.simple_tag
def horizontal_link_is_active(current_path, link_url, is_external=False):
    """Return whether an internal link represents the current path or one of its ancestors."""
    return _link_is_active(current_path, link_url, is_external)


@register.simple_tag
def horizontal_link_active_link(request, links):
    """Return the most specific same-site link matching the current request."""
    active_link = None
    active_path_length = -1

    for item in links:
        link = item.value
        link_url = _internal_link_url(request, link)
        if not _link_is_active(request.path, link_url):
            continue

        target = _normalized_path(link_url)
        if target and len(target) > active_path_length:
            active_link = link
            active_path_length = len(target)

    return active_link


def _iter_dropdown_links(dropdowns):
    for dropdown in dropdowns or []:
        yield dropdown.value.header_value
        yield from dropdown.value.dropdown_items


@register.simple_tag
def primary_nav_active_link(request, dropdowns):
    """Return the most specific internal link matching the localized path."""
    active_link = None
    active_path_length = -1

    for link in _iter_dropdown_links(dropdowns):
        link_url = _internal_link_url(request, link)
        if not _link_is_active(request.path, link_url, strip_locale=True):
            continue

        target = _normalized_path(link_url, strip_locale=True)
        if target and len(target) > active_path_length:
            active_link = link
            active_path_length = len(target)

    return active_link


@register.simple_tag
def navigation_link_is_active(active_link, link):
    return active_link is link


@register.simple_tag
def primary_nav_link_is_current(request, link):
    """Return whether a selected link points to the exact localized path."""
    link_url = _internal_link_url(request, link)
    current = _normalized_path(request.path, strip_locale=True)
    target = _normalized_path(link_url, strip_locale=True)

    return bool(current and target and current == target)


@register.simple_tag
def primary_nav_dropdown_is_active(active_link, dropdown):
    if navigation_link_is_active(active_link, dropdown.header_value):
        return True

    return any(navigation_link_is_active(active_link, item) for item in dropdown.dropdown_items)
