import factory

from django.core.management.base import BaseCommand
from django.core.management import call_command

# Factories
from networkapi.highlights.factory import HighlightFactory
from networkapi.landingpage.factory import LandingPageFactory, SignupFactory
from networkapi.milestones.factory import MilestoneFactory
from networkapi.news.factory import NewsFactory
from networkapi.people.factory import (
    PersonFactory,
    AffiliationFactory,
    InternetHealthIssueFactory,
)
from networkapi.homepage.factory import (
    HomepageFactory,
    HomepageNewsFactory,
    HomepageLeadersFactory,
    HomepageHighlightsFactory,
)

internet_health_issues = [
    'Digital Inclusion',
    'Web Literacy',
    'Open Innovation',
    'Decentralization',
    'Online Privacy and Security',
]


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

        parser.add_argument(
            '--seed',
            action='store',
            dest='seed',
            help='A seed value to pass to Faker before generating data',
        )

    def handle(self, *args, **options):

        if options['delete']:
            call_command('flush_models')

        if options['seed']:
            faker = factory.faker.Faker._get_faker(locale='en-US')
            faker.random.seed(options['seed'])


        self.stdout.write('Generating LandingPage objects')
        opportunity = LandingPageFactory.create(title='opportunity', content='This is placeholder')
        [LandingPageFactory.create(parent=opportunity) for i in range(5)]

        self.stdout.write('Generating LandingPage objects with Signup CTAs')
        [LandingPageFactory.create(parent=opportunity, signup=SignupFactory.create()) for i in range(5)]

        self.stdout.write('Generating Homepage')
        homepage = HomepageFactory.create()

        self.stdout.write('Generating HomepageNews, HomepageHighlights, and HomepageLeaders objects')
        [HomepageNewsFactory.create(homepage=homepage) for i in range(4)]
        [HomepageHighlightsFactory.create(homepage=homepage) for i in range(4)]
        [HomepageLeadersFactory.create(homepage=homepage) for i in range(4)]

        self.stdout.write('Generating Highlight objects')
        [HighlightFactory.create() for i in range(10)]

        self.stdout.write('Generating Milestone objects')
        [MilestoneFactory.create() for i in range(10)]

        self.stdout.write('Generating News objects')
        [NewsFactory.create() for i in range(10)]

        self.stdout.write('Generating five InternetHealthIssue objects')
        issue_objects = []
        for issue in internet_health_issues:
            issue_objects.append(InternetHealthIssueFactory(name=issue))

        self.stdout.write('Generating Person and Affiliation objects')
        for i in range(10):
            person = PersonFactory.create(internet_health_issues=issue_objects)

            for j in range(3):
                AffiliationFactory.create(person=person)

        self.stdout.write('Generating unpublished, expired, and expiring highlights')
        [HighlightFactory.create(unpublished=True) for i in range(4)]
        [HighlightFactory.create(expired=True) for i in range(4)]
        [HighlightFactory.create(has_expiry=True) for i in range(4)]

        self.stdout.write('Generating unpublished, expired, and expiring News')
        [NewsFactory.create(unpublished=True) for i in range(4)]
        [NewsFactory.create(expired=True) for i in range(4)]
        [NewsFactory.create(has_expiry=True) for i in range(4)]
        [NewsFactory.create(is_video=True) for i in range(4)]

        self.stdout.write('Generating featured, unpublished, expired, and expiring People')
        [PersonFactory.create(is_featured=True) for i in range(4)]
        [PersonFactory.create(unpublished=True) for i in range(4)]
        [PersonFactory.create(has_expiry=True) for i in range(4)]
        [PersonFactory.create(expired=True) for i in range(4)]

        self.stdout.write(self.style.SUCCESS('Done!'))
