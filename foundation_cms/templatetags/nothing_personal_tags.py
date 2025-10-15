from django import template
from django.utils.translation import get_language
from wagtail.models import Locale

from foundation_cms.nothing_personal.models import NothingPersonalHomePage

register = template.Library()


@register.simple_tag(takes_context=True)
def nothing_personal_homepage_url(context):
    """
    Returns the URL of the first live NothingPersonalHomePage instance
    in the current locale.
    """
    request = context.get("request")
    current_language = get_language()

    try:
        current_locale = Locale.objects.get(language_code=current_language)
    except Locale.DoesNotExist:
        current_locale = Locale.get_default()

    # Get the page in the current locale
    homepage = NothingPersonalHomePage.objects.live().filter(locale=current_locale).first()

    # If not found in current locale, try default locale
    if not homepage and current_locale != Locale.get_default():
        homepage = NothingPersonalHomePage.objects.live().filter(locale=Locale.get_default()).first()

    if homepage:
        return homepage.get_url(request=request) if request else homepage.get_url()

    return ""
