from itertools import chain, combinations

import factory
from random import randint

from django.conf import settings

from django.core.management.base import BaseCommand
from django.core.management import call_command

# Factories
import networkapi.highlights.factory as highlights_factory
import networkapi.milestones.factory as milestones_factory
import networkapi.news.factory as news_factory
import networkapi.people.factory as people_factory
import networkapi.wagtailpages.factory as wagtailpages_factory
import networkapi.buyersguide.factory as buyersguide_factory

from wagtail_factories import ImageFactory


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


# Create a list of dictionaries containing every factory params permutation possible. ex: [{'group': True},
# {'group': True, 'active': True}, ...]
def generate_variations(factory_model):
    for variation in powerset(factory_model._meta.parameters.keys()):
        yield {k: True for k in variation}


# Create fake data for every permutation possible
def generate_fake_data(factory_model, count):
    for kwargs in generate_variations(factory_model):
        for i in range(count):
            factory_model.create(**kwargs)


class Command(BaseCommand):
    help = 'Generate fake data for local development and testing purposes' \
           'and load it into the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--delete',
            action='store_true',
            dest='delete',
            help="""Delete previous highlights, homepage, landing page,
                milestones, news, people, and products from the database""",
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

        # Seed Faker with the provided seed value or a pseudorandom int between 0 and five million
        if options['seed']:
            seed = options['seed']
        elif settings.RANDOM_SEED is not None:
            seed = settings.RANDOM_SEED
        else:
            seed = randint(0, 5000000)

        print('Seeding Faker with: {}'.format(seed))
        faker = factory.faker.Faker._get_faker(locale='en-US')
        faker.random.seed(seed)

        print('Generating Images')
        [
            ImageFactory.create(
                file__width=1080,
                file__height=720,
                file__color=faker.safe_color_name()
            ) for i in range(20)
        ]

        [app_factory.generate() for app_factory in [
            milestones_factory,
            news_factory,
            highlights_factory,
            people_factory,
            wagtailpages_factory,
            buyersguide_factory
        ]]

        print(self.style.SUCCESS('Done!'))
