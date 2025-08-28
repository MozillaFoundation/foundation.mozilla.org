from django.conf import settings
from wagtail.models import Locale


def get_default_locale():
    """
    We defer this logic to a function so that we can call it on demand without
    running into "the db is not ready for queries yet" problems.
    """
    DEFAULT_LOCALE = Locale.objects.get(language_code=settings.LANGUAGE_CODE)
    DEFAULT_LOCALE_ID = DEFAULT_LOCALE.id
    return (
        DEFAULT_LOCALE,
        DEFAULT_LOCALE_ID,
    )
