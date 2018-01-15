from django.core.management.base import BaseCommand

from networkapi.highlights.factory import HighlightFactory
from networkapi.highlights.models import Highlight
from networkapi.homepage.factory import (
    HomepageFactory,
    HomepageNewsFactory,
    HomepageLeadersFactory,
    HomepageHighlightsFactory
)
from networkapi.homepage.models import Homepage
from networkapi.landingpage.factory import LandingPageFactory, SignupFactory
from networkapi.landingpage.models import LandingPage, Signup
from networkapi.milestones.factory import MilestoneFactory
from networkapi.milestones.models import Milestone
from networkapi.news.factory import NewsFactory
from networkapi.news.models import News
from networkapi.people.factory import PersonFactory, AffiliationFactory
from networkapi.people.models import Person, Affiliation


class Command(BaseCommand):
    help = 'Generate fake data for local development and testing purposes' \
           'and load it into the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--delete',
            action='store_true',
            dest='delete',
            help='Delete previous highlights, homepage, landing page, milestones, news and people from the database',
        )

    def handle(self, *args, **options):

        if options['delete']:
            Homepage.objects.all().delete()
            LandingPage.objects.all().delete()
            Signup.objects.all().delete()
            Highlight.objects.all().delete()
            News.objects.all().delete()
            Milestone.objects.all().delete()
            Person.objects.all().delete()
            Affiliation.objects.all().delete()

        # Create the landing page
        LandingPageFactory.create()
        SignupFactory.create()

        # Create 4 elements for each categories on homepage
        homepage = HomepageFactory.create()
        [HomepageNewsFactory.create(homepage=homepage) for i in range(4)]
        [HomepageHighlightsFactory.create(homepage=homepage) for i in range(4)]
        [HomepageLeadersFactory.create(homepage=homepage) for i in range(4)]

        # Create more content default content
        [HighlightFactory.create() for i in range(10)]
        [MilestoneFactory.create() for i in range(10)]
        [NewsFactory.create() for i in range(10)]
        [PersonFactory.create() for i in range(10)]
        # TODO AFFILIATION NEEDS TO BE ASSOCIATED TO PEOPLE
        [AffiliationFactory.create() for i in range(10)]

        # Create Highlights with specific traits
        [HighlightFactory.create(unpublished=True) for i in range(4)]
        [HighlightFactory.create(expired=True) for i in range(4)]
        [HighlightFactory.create(has_expiry=True) for i in range(4)]

        # Create News with specific traits
        [NewsFactory.create(unpublished=True) for i in range(4)]
        [NewsFactory.create(expired=True) for i in range(4)]
        [NewsFactory.create(has_expiry=True) for i in range(4)]
        [NewsFactory.create(is_video=True) for i in range(4)]

        # Create People with specific traits
        [PersonFactory.create(is_featured=True) for i in range(4)]
        [PersonFactory.create(unpublished=True) for i in range(4)]
        [PersonFactory.create(has_expiry=True) for i in range(4)]
        [PersonFactory.create(expired=True) for i in range(4)]
