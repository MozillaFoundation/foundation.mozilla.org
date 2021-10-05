from networkapi.wagtailpages.utils import get_default_locale


class LocalizedSnippet():

    DEFAULT_LOCALE = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.DEFAULT_LOCALE is None:
            (DEFAULT_LOCALE, DEFAULT_LOCALE_ID) = get_default_locale()
            self.DEFAULT_LOCALE = DEFAULT_LOCALE

    @property
    def original(self):
        try:
            return self.get_translation(self.DEFAULT_LOCALE)
        except AttributeError:
            return self
