from django import template

register = template.Library()

DEFAULT_LOCALE = 'en_US'

mappings = {
    'en': 'en_US',
    'de': 'de_DE',
    'es': 'es_ES',
    'fr': 'fr_FR',
    'fy-NL': 'fy_NL',
    'nl': 'nl_NL',
    'pl': 'pl_PL',
    'pt': 'pt_BR',  # our main focus is Brazilian Portuguese
}


# This filter turns Wagtail language codes into OpenGraph locale strings
@register.filter
def to_opengraph_locale(value):
    try:
        return mappings[value]
    except AttributeError:
        return DEFAULT_LOCALE
