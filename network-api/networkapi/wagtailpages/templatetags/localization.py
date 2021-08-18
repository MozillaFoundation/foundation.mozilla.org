import locale
import unicodedata

from django import template
from django.conf import settings
from django.utils.translation import get_language_info
from wagtail.contrib.routable_page.templatetags.wagtailroutablepage_tags import routablepageurl
from networkapi.wagtailpages.utils import get_language_from_request

register = template.Library()

mappings = {
    'en': 'en_US',
    'de': 'de_DE',
    'es': 'es_ES',
    'fr': 'fr_FR',
    'fy-NL': 'fy_NL',
    'nl': 'nl_NL',
    'pl': 'pl_PL',
    'pt-BR': 'pt_BR',
}

DEFAULT_LOCALE_CODE = settings.LANGUAGE_CODE
DEFAULT_LOCALE = mappings.get(DEFAULT_LOCALE_CODE)


# This filter turns Wagtail language codes into OpenGraph locale strings
@register.filter
def to_opengraph_locale(value):
    try:
        return mappings[value]
    except AttributeError:
        return DEFAULT_LOCALE


# Generates a sorted list of currently supported locales. For each locale, the list
# contains the locale code and the local name of the locale.
# To sort the list by local names, we use:
# - Case folding, in order to do case-insensitive comparison, and more.
# - String normalization using the Normalization Form Canonical Decomposition, to compare
#   canonical equivalence (e.g. without diacritics)
@register.simple_tag()
def get_local_language_names():
    locale.setlocale(locale.LC_ALL, "C.UTF-8")
    languages = []
    for lang in settings.LANGUAGES:
        languages.append([lang[0], get_language_info(lang[0])['name_local']])
    return sorted(languages, key=lambda x: locale.strxfrm(unicodedata.normalize('NFD', x[1])).casefold())


# Get the url for a page, but with the locale code removed.
@register.simple_tag()
def get_unlocalized_url(page, locale):
    return page.get_url().replace(f'/{locale}/', '/', 1)


# Force-relocalize a URL
@register.simple_tag(takes_context=True)
def relocalized_url(context, url):
    request = context['request']
    locale_code = get_language_from_request(request);
    if locale_code == DEFAULT_LOCALE_CODE:
        return url
    return url.replace(f'/{DEFAULT_LOCALE_CODE}/', f'/{locale_code}/')


# Overcome a limitation of the routablepageurl tag
@register.simple_tag(takes_context=True)
def localizedroutablepageurl(context, page, url_name, *args, **kwargs):
    url = relocalized_url(
        context,
        routablepageurl(context, page, url_name, *args, **kwargs)
    )
    return url
