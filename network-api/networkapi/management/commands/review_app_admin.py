"""
Management command called during the Heroku Review App post-deployment phase.
Creates an admin user and prints the password to the build logs.
"""
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from factory import Faker
from django.contrib.auth.models import User
from django.conf import settings
import re

import requests


class Command(BaseCommand):
    help = 'Create a superuser for use on Heroku review apps'

    def handle(self, *args, **options):
        try:
            User.objects.get(username='admin')
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
            User.objects.create_superuser('admin', 'admin@example.com', password)

            reviewapp_name = settings.HEROKU_APP_NAME
            m = re.search(r'\d+', reviewapp_name)
            pr_number = m.group()

            # Get PR's title from Github
            r = requests.get(f"https://api.github.com/repos/mozilla/foundation.mozilla.org/pulls/{pr_number}")
            pr_title = r.json()['title']

            slack_payload = {
                "attachments": [
                    {
                        "fallback": "New review app deployed :rocket:\n"
                                    f"PR {pr_number}: {pr_title}\n"
                                    f"Login: admin\n"
                                    f"Password: {password}\n"
                                    f"URL: https://{reviewapp_name}.herokuapp.com",
                        "pretext":  "New review app deployed :rocket:",
                        "title":    f"PR {pr_number}: {pr_title}\n",
                        "text":     "Login: admin\n"
                                    f"Password: {password}\n",
                        "color":    "#7CD197",
                        "actions": [
                            {
                                "type": "button",
                                "text": "Open review app",
                                "url": f"https://{reviewapp_name}.herokuapp.com"
                            },
                            {
                                "type": "button",
                                "text": "Open PR on Github",
                                "url": f"https://github.com/mozilla/foundation.mozilla.org/pull/{pr_number}"
                            }
                        ]
                    }
                ]
            }

            requests.post('https://hooks.slack.com/services/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',
                          json=slack_payload,
                          headers={'Content-Type': 'application/json'}
                          )

            print("Done!")
