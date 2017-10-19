from django.core.management.base import BaseCommand
from django.core.management import call_command
from mezzanine.conf import settings


class Command(BaseCommand):
    help = 'migrate the database if needed, and optionally seed' \
        'the database using app/networkapi/fixtures/test_data.json'

    def handle(self, *args, **options):

        call_command('migrate')

        if settings.LOAD_FIXTURE:
            call_command('update_site_domain')
            call_command('loaddata', 'app/networkapi/fixtures/test_data.json')
