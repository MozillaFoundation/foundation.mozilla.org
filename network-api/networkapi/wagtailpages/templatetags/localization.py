from django import template

register = template.Library()

DEFAULT_LOCALE = 'en_US'

mappings = {
    'en': 'en_US',
    'fr': 'fr_FR',
    'es': 'es_ES',
    'de': 'de_DE',
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
