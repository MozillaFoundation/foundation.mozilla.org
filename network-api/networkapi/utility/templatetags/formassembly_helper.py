from django import template
from django.utils.translation import get_language

register = template.Library()


@register.simple_tag(name="fa_locale_code")
def fa_locale_code():
    """
    Returns the FormAssembly locale code for the current language.
    """

    fa_default = "en_US"

    # key: available locales on fo.mo
    # value: ISO code used by FormAssembly https://app.formassembly.com/translate
    mappings = {
        "en": fa_default,
        "de": "de",
        "es": "es",
        "fr": "fr",
        "fy-NL": None,
        "nl": "nl",
        "pl": "pl",
        "pt-BR": "pt_BR",
        "sw": None,
    }

    fa_supported_locale = mappings.get(get_language())

    return fa_supported_locale if fa_supported_locale else fa_default
