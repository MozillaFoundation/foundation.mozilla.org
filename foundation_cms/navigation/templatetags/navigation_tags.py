from django import template

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
