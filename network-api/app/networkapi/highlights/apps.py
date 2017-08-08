from django.apps import AppConfig


class HighlightsConfig(AppConfig):
    name = 'networkapi.highlights'
    verbose_name = 'highlights'

    def ready(self):
        from networkapi.highlights.signals import setup_signals
        setup_signals()
