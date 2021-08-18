from django.conf import settings
from wagtail.core.models import Locale


class LocalizedSnippet():

    DEFAULT_LOCALE = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.DEFAULT_LOCALE is None:
            self.DEFAULT_LOCALE = Locale.objects.get(language_code=settings.LANGUAGE_CODE)

    @property
    def original(self):
        try:
            return self.get_translation(self.DEFAULT_LOCALE)
        except AttributeError:
            return self
