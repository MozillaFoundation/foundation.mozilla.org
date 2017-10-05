from django.apps import AppConfig


class HighlightsConfig(AppConfig):
    name = 'networkapi.highlights'
    verbose_name = 'highlights'

    def ready(self):
        pass
