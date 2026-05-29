from django.apps import AppConfig


class SearchConfig(AppConfig):
    name = "foundation_cms.search"

    def ready(self):
        from . import signals  # noqa: F401
