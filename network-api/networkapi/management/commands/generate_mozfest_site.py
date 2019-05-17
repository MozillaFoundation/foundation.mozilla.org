from django.conf import settings
from django.core.management.base import BaseCommand
from wagtail.core.models import Site as WagtailSite
from networkapi.mozfest.models import MozfestPrimaryPage
import networkapi.mozfest.factory as mozfest_factory
import random


class Command(BaseCommand):
    help = 'Generate a site and content for the Mozfest sub-site.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--seed',
            action='store',
            dest='seed',
            help='A seed value to pass to Faker before generating data',
        )

    def handle(self, *args, **options):

        if options['seed']:
            seed = options['seed']
        elif settings.RANDOM_SEED is not None:
            seed = settings.RANDOM_SEED
        else:
            seed = random.randint(0, 5000000)

        print('Dropping all Mozfest pages')
        MozfestPrimaryPage.objects.all().delete()
        try:
            print('Dropping Mozfest Site')
            WagtailSite.objects.get(site_name='Mozilla Festival').delete()
        except WagtailSite.DoesNotExist:
            pass

        mozfest_factory.generate(seed)