from django.apps import AppConfig


class PeopleConfig(AppConfig):
    name = 'networkapi.people'
    verbose_name = 'people'

    def ready(self):
        pass
