from django.core.management.base import BaseCommand
from django.core.management import call_command
from mezzanine.conf import settings


class Command(BaseCommand):
    help = 'migrate the database if needed, and' \
        'generate a full set of fake model data'

    def handle(self, *args, **options):

        call_command('migrate')

        if settings.EXECUTE_FAKE_DATA:
            call_command('update_site_domain')
            call_command('load_fake_data', '--delete')
