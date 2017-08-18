from django.apps import AppConfig


class PeopleConfig(AppConfig):
    name = 'networkapi.people'
    verbose_name = 'people'

    def ready(self):
        from networkapi.people.signals import setup_signals
        setup_signals()
