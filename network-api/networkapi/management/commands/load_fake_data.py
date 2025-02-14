import random
from os.path import abspath, dirname, join

import factory
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from taggit.models import Tag

# Factories
import networkapi.donate.factory as donate_factory
import networkapi.highlights.factory as highlights_factory
import networkapi.mozfest.factory as mozfest_factory
import networkapi.nav.factories as nav_factory
import networkapi.news.factory as news_factory
import networkapi.wagtailpages.factory as wagtailpages_factory
from networkapi.utility.faker.helpers import reseed
from networkapi.wagtailpages.utils import create_wagtail_image


class Command(BaseCommand):
    help = "Generate fake data for local development and testing purposes" "and load it into the database"

    def add_arguments(self, parser):
        parser.add_argument(
            "--delete",
            action="store_true",
            dest="delete",
            help="""Delete previous highlights, homepage, landing page,
                    news, and products from the database""",
        )

        parser.add_argument(
            "--seed",
            action="store",
            dest="seed",
            help="A seed value to pass to Faker before generating data",
        )

    def handle(self, *args, **options):
        if options["delete"]:
            call_command("flush_models")

        faker = factory.faker.Faker._get_faker(locale="en-US")

        # Seed Faker with the provided seed value or a pseudorandom int between 0 and five million
        if options["seed"]:
            seed = options["seed"]
        elif settings.RANDOM_SEED is not None:
            seed = settings.RANDOM_SEED
        else:
            seed = random.randint(0, 5000000)

        print(f"Seeding random numbers with: {seed}")

        reseed(seed)

        # Create one PNI product for every image we have in our media folder
        product_images = [
            "babymonitor.jpg",
            "drone.jpg",
            "nest.jpg",
            "teddy.jpg",
            "echo.jpg",
        ]

        for image in product_images:
            image_path = abspath(
                join(
                    dirname(__file__),
                    f"../../../media/images/placeholders/products/{image}",
                )
            )
            create_wagtail_image(image_path, collection_name="pni products")

        [
            app_factory.generate(seed)
            for app_factory in [
                news_factory,
                highlights_factory,
                wagtailpages_factory,
                mozfest_factory,
                donate_factory,
                nav_factory,
            ]
        ]

        print(self.style.SUCCESS("Done!"))
