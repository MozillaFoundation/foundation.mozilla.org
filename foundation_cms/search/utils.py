from wagtail.models import Locale
from wagtail.search import get_search_backend
from django.conf import settings

SUPPORTED_SEARCH_LANGUAGES = {
    "nl": "dutch",
    "en": "english", 
    "fr": "french",
    "de": "german",
    "pt": "portuguese",
    "es": "spanish",
}

def get_search_backend_for_locale(locale_code=None):
    """
    Get the appropriate search backend for a given locale.
    Uses language-specific backend if available, otherwise falls back to 'simple'.
    """
    if locale_code is None:
        try:
            locale = Locale.get_active()
            locale_code = locale.language_code
        except:
            locale_code = "en"
    
    # Check if we have a specific backend for this language
    if locale_code in SUPPORTED_SEARCH_LANGUAGES:
        try:
            backend = get_search_backend(backend=locale_code)
            return backend, locale_code
        except Exception:
            pass  # Fall through to default
    
    # Fallback to default backend (simple)
    return get_search_backend(), "simple"

def get_available_search_locales():
    """
    Get list of locales that have dedicated search backends.
    """
    return list(SUPPORTED_SEARCH_LANGUAGES.keys())

def should_use_locale_backend(locale_code):
    """
    Check if we should use a locale-specific backend for search.
    """
    return locale_code in SUPPORTED_SEARCH_LANGUAGES

def get_search_config_for_locale(locale_code):
    """
    Get the PostgreSQL search configuration name for a locale.
    """
    return SUPPORTED_SEARCH_LANGUAGES.get(locale_code, 'simple')
