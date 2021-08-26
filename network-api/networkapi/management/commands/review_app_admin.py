"""
Management command called during the Heroku Review App post-deployment phase.
Creates an admin user and prints the password to the build logs.
"""
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from factory import Faker
from django.contrib.auth.models import User
from django.conf import settings

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
            )
            User.objects.create_superuser('admin', 'admin@example.com', str(password))

            reviewapp_name = settings.HEROKU_APP_NAME
            pr_number = settings.HEROKU_PR_NUMBER
            branch_name = settings.HEROKU_BRANCH

            # Review apps created when opening a PR
            if pr_number:
                # Get PR's title from Github
                token = settings.GITHUB_TOKEN
                org = 'mozilla'
                repo = 'foundation.mozilla.org'
                headers = {'Authorization': f'token {token}'}
                r = requests.get(f'https://api.github.com/repos/{org}/{repo}/pulls/{pr_number}', headers=headers)
                r.raise_for_status()
                try:
                    pr_title = ' - ' + r.json()['title']
                except KeyError:
                    pr_title = ''

                for label in r.json()['labels']:
                    if label['name'] == 'dependencies':
                        pre_title = ':robot_face: *[Dependabot]*'
                        break
                else:
                    pre_title = ':computer: *[Devs]*'
                message_title = f'*PR {pr_number}{pr_title}*\n'
                github_url = f'https://github.com/mozilla/foundation.mozilla.org/pull/{pr_number}'
                github_button_text = 'View PR on Github'

            # Review apps created from Heroku to deploy a branch
            else:
                pre_title = ':computer: *[Devs]*'
                message_title = f'Branch: {branch_name}\n'
                github_url = f'https://github.com/mozilla/foundation.mozilla.org/tree/{branch_name}'
                github_button_text = 'View branch on Github'

            slack_payload = {
                'blocks': [
                    {
                        'type': 'section',
                        'text': {
                            'type': 'mrkdwn',
                            'text': f'{pre_title} {message_title}'
                                    'This new review app will be ready in a minute!\n'
                                    '*Login:* admin\n'
                                    f'*Password:* {str(password)}\n'
                        }
                    },
                    {
                        'type': 'actions',
                        'elements': [
                            {
                                'type': 'button',
                                'text': {
                                    'type': 'plain_text',
                                    'text': 'View review app'
                                },
                                'url': f'https://{reviewapp_name}.herokuapp.com'
                            },
                            {
                                'type': 'button',
                                'text': {
                                    'type': 'plain_text',
                                    'text': f'{github_button_text}',
                                },
                                'url': f'{github_url}'
                            }
                        ]
                    },
                    {
                        'type': 'divider',
                    }
                ]
            }

            slack_webhook = settings.SLACK_WEBHOOK_RA
            r = requests.post(f'{slack_webhook}',
                              json=slack_payload,
                              headers={'Content-Type': 'application/json'}
                              )

            # Raise if post request was a 4xx or 5xx
            r.raise_for_status()
            print('Done!')
