"""
Management command called during the Heroku Review App post-deployment phase.
Creates an admin user and prints the password to the build logs.
"""
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from factory import Faker
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Create a superuser for use on Heroku review apps'

    def handle(self, *args, **options):
        try:
            User.objects.get(username='admin')
            self.stdout.write('super user already exists')
        except ObjectDoesNotExist:
            password = Faker(
                'password',
                length=16,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True
            ).generate({})
            User.objects.create_superuser('admin', 'admin@example.com', password)
            self.stdout.write(f'superuser created. Password: {password}')
