from django.apps import AppConfig


class NewsConfig(AppConfig):
    name = 'networkapi.news'
    verbose_name = 'news'

    def ready(self):
        from networkapi.news.signals import setup_signals
        setup_signals()
