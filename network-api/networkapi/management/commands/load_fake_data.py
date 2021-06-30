import factory
import random
from os.path import abspath, dirname, join

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings

from taggit.models import Tag

# Factories
import networkapi.highlights.factory as highlights_factory
import networkapi.news.factory as news_factory
import networkapi.wagtailpages.factory as wagtailpages_factory
import networkapi.mozfest.factory as mozfest_factory

from networkapi.wagtailpages.factory.image_factory import ImageFactory
from networkapi.wagtailpages.utils import create_wagtail_image
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
                    news, and products from the database""",
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
        images = [
            ImageFactory.create(
                file__width=1080,
                file__height=720,
                file__color=faker.safe_color_name()
            ) for i in range(20)
        ]
        social_share_tag, created = Tag.objects.get_or_create(name='social share image')
        images[0].tags.add(social_share_tag)

        # Create one PNI product for every image we have in our media folder
        product_images = ['babymonitor.jpg', 'drone.jpg', 'nest.jpg',
                          'teddy.jpg', 'echo.jpg']

        for image in product_images:
            image_path = abspath(join(dirname(__file__), f'../../../media/images/placeholders/products/{image}'))
            create_wagtail_image(
                image_path,
                collection_name='pni products'
            )

        [app_factory.generate(seed) for app_factory in [
            news_factory,
            highlights_factory,
            wagtailpages_factory,
            mozfest_factory
        ]]

        print(self.style.SUCCESS('Done!'))
