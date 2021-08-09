from django.conf import settings
from wagtail.core.models import Locale

DEFAULT_LOCALE = Locale.objects.get(language_code=settings.LANGUAGE_CODE)


class LocalizedSnippet():
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def original(self):
        try:
            return self.get_translation(DEFAULT_LOCALE)
        except AttributeError:
            return self

