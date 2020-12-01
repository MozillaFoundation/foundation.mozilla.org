import factory
import random

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings

# Factories
import networkapi.highlights.factory as highlights_factory
import networkapi.milestones.factory as milestones_factory
import networkapi.news.factory as news_factory
import networkapi.wagtailpages.factory as wagtailpages_factory
import networkapi.buyersguide.factory as buyersguide_factory
import networkapi.mozfest.factory as mozfest_factory

from networkapi.wagtailpages.factory.image_factory import ImageFactory
from networkapi.utility.faker.helpers import reseed


class Command(BaseCommand):
    help = 'Generate fake data for local development and testing purposes' \
           'and load it into the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--delete',
            action='store_true',
            dest='delete',
            help="""Delete previous highlights, homepage, landing page,
                milestones, news, and products from the database""",
        )

        parser.add_argument(
            '--seed',
            action='store',
            dest='seed',
            help='A seed value to pass to Faker before generating data',
        )

    def handle(self, *args, **options):

        if options['delete']:
            call_command('flush_models')

        faker = factory.faker.Faker._get_faker(locale='en-US')

        # Seed Faker with the provided seed value or a pseudorandom int between 0 and five million
        if options['seed']:
            seed = options['seed']
        elif settings.RANDOM_SEED is not None:
            seed = settings.RANDOM_SEED
        else:
            seed = random.randint(0, 5000000)

        print(f'Seeding random numbers with: {seed}')

        reseed(seed)

        print('Generating Images')
        [
            ImageFactory.create(
                file__width=1080,
                file__height=720,
                file__color=faker.safe_color_name()
            ) for i in range(20)
        ]

        [app_factory.generate(seed) for app_factory in [
            milestones_factory,
            news_factory,
            highlights_factory,
            wagtailpages_factory,
            buyersguide_factory,
            mozfest_factory
        ]]

        print(self.style.SUCCESS('Done!'))
