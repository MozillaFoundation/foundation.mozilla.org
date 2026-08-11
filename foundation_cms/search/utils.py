from wagtail.search.backends import get_search_backend

SUPPORTED_SEARCH_LANGUAGES = {
    "en": "english",
    "de": "german",
    "es": "spanish",
    "fr": "french",
    "nl": "dutch",
    "pt-BR": "portuguese",
}

SEARCH_SORTS = ("relevance", "newest", "oldest")

SECTION_SLUGS = {
    "all": None,
    "what-we-do": "what-we-do",
    "research": "research",
    "press-release": "press-release",
    "event": "event",
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


def normalize_sort(value, default="relevance"):
    value = (value or default).strip().lower()
    return value if value in SEARCH_SORTS else default


def normalize_content_type(value, default="all"):
    value = (value or default).strip().lower()
    return value if value in SECTION_SLUGS else default


def normalize_topic(value):
    return (value or "").strip().lower()
