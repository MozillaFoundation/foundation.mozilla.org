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
    parsed_url = urlsplit(url or "")
    if parsed_url.scheme or parsed_url.netloc:
        return None

    path = parsed_url.path
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


@register.simple_tag
def horizontal_link_is_active(current_path, link_url, is_external=False):
    """Return whether an internal link represents the current path or one of its ancestors."""
    return _link_is_active(current_path, link_url, is_external)


@register.simple_tag
def horizontal_link_active_url(current_path, links):
    """Return the URL of the most specific internal link matching the current path."""
    active_url = None
    active_path_length = -1

    for item in links:
        link = item.value
        if not horizontal_link_is_active(current_path, link.url, link.is_external):
            continue

        target = _normalized_path(link.url)
        if target and len(target) > active_path_length:
            active_url = link.url
            active_path_length = len(target)

    return active_url


def _iter_dropdown_links(dropdowns):
    for dropdown in dropdowns or []:
        yield dropdown.value.header_value
        yield from dropdown.value.dropdown_items


@register.simple_tag
def primary_nav_active_link(current_path, dropdowns):
    """Return the most specific internal link matching the localized path."""
    active_link = None
    active_path_length = -1

    for link in _iter_dropdown_links(dropdowns):
        if not _link_is_active(current_path, link.url, link.is_external, strip_locale=True):
            continue

        target = _normalized_path(link.url, strip_locale=True)
        if target and len(target) > active_path_length:
            active_link = link
            active_path_length = len(target)

    return active_link


@register.simple_tag
def primary_nav_link_is_active(active_link, link):
    return active_link is link


@register.simple_tag
def primary_nav_link_is_current(current_path, link):
    """Return whether a selected link points to the exact localized path."""
    if not link or link.is_external:
        return False

    return _normalized_path(current_path, strip_locale=True) == _normalized_path(link.url, strip_locale=True)


@register.simple_tag
def primary_nav_dropdown_is_active(active_link, dropdown):
    if primary_nav_link_is_active(active_link, dropdown.header_value):
        return True

    return any(primary_nav_link_is_active(active_link, item) for item in dropdown.dropdown_items)
