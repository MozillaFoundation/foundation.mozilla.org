from wagtail.search.backends import get_search_backend

SUPPORTED_SEARCH_LANGUAGES = {
    "en": "english",
    "de": "german",
    "es": "spanish",
    "fr": "french",
    "nl": "dutch",
    "pt-BR": "portuguese",
}


def get_search_backend_for_locale(locale_code=None):
    """
    Get the appropriate search backend for a given locale.
    Uses language-specific backend if available, otherwise falls back to 'simple'.
    """
    # Check if we have a specific backend for this language
    if locale_code in SUPPORTED_SEARCH_LANGUAGES:
        try:
            return get_search_backend(backend=locale_code), locale_code
        except Exception:
            pass

    # Fallback to default backend
    return get_search_backend(), "default"
