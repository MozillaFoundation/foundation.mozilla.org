from django.core.management.base import BaseCommand

from networkapi.milestones.factory import MilestoneFactory
from networkapi.news.factory import NewsFactory


class Command(BaseCommand):
    help = 'Generate fake data for local development and testing purposes' \
           'and load it into the database'

    def handle(self, *args, **options):
        [MilestoneFactory.create() for i in range(2)]
        [NewsFactory.create() for i in range(4)]
        NewsFactory.create(is_featured=True)
