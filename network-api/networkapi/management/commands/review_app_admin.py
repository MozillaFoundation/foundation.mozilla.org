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
            ).generate({})
            User.objects.create_superuser('admin', 'admin@example.com', password)

            reviewapp_name = settings.HEROKU_APP_NAME
            pr_number = settings.HEROKU_PR_NUMBER
            branch_name = settings.HEROKU_BRANCH

            # As of 01/2020 we can only get the PR number if the review app was automatically created
            # (https://devcenter.heroku.com/articles/github-integration-review-apps#injected-environment-variables).
            # For review app manually created, we have to use the branch name instead.
            if pr_number:
                # Get PR's title from Github
                token = settings.GITHUB_TOKEN
                org = 'mozilla'
                repo = 'foundation.mozilla.org'
                headers = {'Authorization': f'token {token}'}
                r = requests.get(f'https://api.github.com/repos/{org}/{repo}/pulls/{pr_number}', headers=headers)
                r.raise_for_status()
                try:
                    pr_title = ': ' + r.json()['title']
                except KeyError:
                    pr_title = ''

                for label in r.json()['labels']:
                    if label['name'] == 'dependencies':
                        color = '#BA55D3'
                        break
                else:
                    color = '#7CD197'
                fallback_text = f'''New review app deployed: It will be ready in a minute!\n
                                                PR {pr_number}{pr_title}\n
                                                Login: admin\n
                                                Password: {password}\n
                                                URL: https://{reviewapp_name}.herokuapp.com'''
                message_title = f'PR {pr_number}{pr_title}\n'
                github_url = f'https://github.com/mozilla/foundation.mozilla.org/pull/{pr_number}'
                github_button_text = 'View PR on Github'

            else:
                color = '#7CD197'
                fallback_text = f'''New review app deployed: It will be ready in a minute!\n
                                                Branch: {branch_name}\n
                                                Login: admin\n
                                                Password: {password}\n
                                                URL: https://{reviewapp_name}.herokuapp.com'''
                message_title = f'Branch: {branch_name}\n'
                github_url = f'https://github.com/mozilla/foundation.mozilla.org/tree/{branch_name}'
                github_button_text = 'View branch on Github'

            slack_payload = {
                'attachments': [
                    {
                        'fallback': f'{fallback_text}',
                        'pretext':  'New review app deployed. It will be ready in a minute!',
                        'title':    f'{message_title}',
                        'text':     'Login: admin\n'
                                    f'Password: {password}\n',
                        'color':    f'{color}',
                        'actions': [
                            {
                                'type': 'button',
                                'text': 'View review app',
                                'url': f'https://{reviewapp_name}.herokuapp.com'
                            },
                            {
                                'type': 'button',
                                'text': f'{github_button_text}',
                                'url': f'{github_url}'
                            }
                        ]
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
