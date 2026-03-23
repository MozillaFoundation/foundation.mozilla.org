from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def translated_footer(context, footer):
    """
    Return a translated version of `footer` for the current page locale when available.
    Falls back to the original footer.
    """
    if not footer:
        return None

    page = context.get("page")
    locale = getattr(page, "locale", None)
    if not locale:
        return footer

    if getattr(footer, "locale_id", None) == locale.id:
        return footer

    translated = footer.get_translation_or_none(locale)
    return translated or footer
