from urllib.parse import urlsplit

from django import template
from wagtail.models import Locale

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
    locale = getattr(page, "locale", None) or Locale.get_active()

    if getattr(menu, "locale_id", None) == locale.id:
        return menu

    translated = menu.get_translation_or_none(locale)
    return translated or menu


def _normalized_path(url):
    path = urlsplit(url or "").path
    if not path:
        return None
    if path == "/":
        return path
    return f"/{path.strip('/')}"


@register.simple_tag
def horizontal_link_is_active(current_path, link_url, is_external=False):
    """Return whether an internal link represents the current path or one of its ancestors."""
    if is_external:
        return False

    current = _normalized_path(current_path)
    target = _normalized_path(link_url)
    if not current or not target:
        return False
    if target == "/":
        return current == target
    return current == target or current.startswith(f"{target}/")


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
