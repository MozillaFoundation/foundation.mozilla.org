"""
Management command called during the Heroku Review App post-deployment phase.
Creates an admin user and prints the password to the build logs.
"""
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from factory import Faker
from django.contrib.auth.models import User

import requests


class Command(BaseCommand):
    help = 'Create a superuser for use on Heroku review apps'

    def handle(self, *args, **options):
        try:
            User.objects.get(username='NewTest')
            print('super user already exists')
        except ObjectDoesNotExist:
            password = Faker(
                'password',
                length=16,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True
            ).generate({})
            User.objects.create_superuser('NewTest', 'admin@example.com', password)

            slack_payload = {"text": f"New review app with {password}"}
            print(password)

            requests.post('https://hooks.slack.com/services/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',
                              json=slack_payload, headers={'Content-Type': 'application/json'})
