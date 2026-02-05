from django import template
from django.conf import settings
from wagtail.models import Locale

register = template.Library()

DEFAULT_LOCALE_CODE = settings.LANGUAGE_CODE


@register.simple_tag(takes_context=True)
def localized_url(context, url, language_code=None):
    """
    Localize a non-page URL by replacing the locale prefix.
    """
    request = context.get("request")
    if not request:
        return url

    if not language_code:
        language_code = Locale.get_active().language_code

    if language_code == DEFAULT_LOCALE_CODE:
        return url

    return url.replace(f"/{DEFAULT_LOCALE_CODE}/", f"/{language_code}/")
