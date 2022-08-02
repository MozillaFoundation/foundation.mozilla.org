from django.contrib.auth import models as auth_models
from django.core.management import base as management_base


class Command(management_base.BaseCommand):
    help = 'Create a superuser for use in local development'

    def handle(self, *args, **options):
        try:
            auth_models.User.objects.get(username='admin')
            print('Superuser `admin` already exists.')
        except auth_models.User.DoesNotExist:
            auth_models.User.objects.create_superuser('admin', 'admin@example.com', 'admin')
            print("\nCreated superuser `admin` with password `admin`.")
