import django
import functools

from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.translation.trans_real import accept_language_re


# WARNING: this is not necessarily a good idea, but is the only way to override
# Django's default behaviour of requiring language codes to be lowercased.
# We have to modify the core Django method, because we have no way to replace
# all the core functionality that relies on this - e.g., url resolvers that
# the Django admin and third party apps use.
# A fix upstream has been asked in https://code.djangoproject.com/ticket/31795


def language_code_to_iso_3166(language):
    """Turn a language name (en-us) into an ISO 3166 format (en-US)."""
    language, _, country = language.lower().partition('-')
    if country:
        return f'{language}-{country.upper()}'
    return language


def to_language(locale):
    """Turn a locale name (en_US) into a language name (en-US)."""
    return locale.replace('_', '-')


@functools.lru_cache(maxsize=1000)
def parse_accept_lang_header(lang_string):
    """
    Parse the lang_string, which is the body of an HTTP Accept-Language
    header, and return a tuple of (lang, q-value), ordered by 'q' values.
    Return an empty tuple if there are any format errors in lang_string.
    """
    result = []
    pieces = accept_language_re.split(lang_string.lower())
    if pieces[-1]:
        return ()
    for i in range(0, len(pieces) - 1, 3):
        first, lang, priority = pieces[i:i + 3]
        if first:
            return ()
        if priority:
            priority = float(priority)
        else:
            priority = 1.0
        result.append((language_code_to_iso_3166(lang), priority))
    result.sort(key=lambda k: k[1], reverse=True)
    return tuple(result)


# Replace some functions in django.utils.translation.trans_real with our own
# versions that support a language in the form en-US instead of en-us.
django.utils.translation.trans_real.to_language = to_language
django.utils.translation.trans_real.parse_accept_lang_header = parse_accept_lang_header
