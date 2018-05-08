import factory
from random import randint

from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from django.core.management import call_command

from wagtail.core.models import Site, Page

# Factories
from networkapi.highlights.factory import HighlightFactory
from networkapi.landingpage.factory import LandingPageFactory, SignupFactory
from networkapi.campaign.factory import CampaignFactory, PetitionFactory
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
from networkapi.wagtailpages.factory import (
    WagtailHomepageFactory,
    PrimaryPageFactory,
    OpportunityPageFactory,
    StyleguideFactory, PeoplePageFactory, NewsPageFactory, InitiativesPageFactory, MiniSiteNameSpaceFactory,
    CampaignPageFactory)
from networkapi.wagtailpages.models import Homepage

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

        # Seed Faker with the provided seed value or a pseudorandom int between 0 and five million
        if options['seed']:
            seed = options['seed']
        else:
            seed = randint(0, 5000000)

        self.stdout.write('Seeding Faker with: {}'.format(seed))
        faker = factory.faker.Faker._get_faker(locale='en-US')
        faker.random.seed(seed)

        self.stdout.write('Generating LandingPage objects')
        opportunity = LandingPageFactory.create(title='Opportunity', content='A placeholder, this is.')
        [LandingPageFactory.create(parent=opportunity) for i in range(5)]

        self.stdout.write('Generating LandingPage objects with Signup CTAs')
        [LandingPageFactory.create(parent=opportunity, signup=SignupFactory.create()) for i in range(5)]

        self.stdout.write('Generating CampaignPage objects')
        campaigns = LandingPageFactory.create(title='Campaigns', content='Placeholder page')
        [CampaignFactory.create(parent=campaigns) for i in range(3)]

        self.stdout.write('Generating CampaignPage objects with known titles')
        important_issue = LandingPageFactory.create(parent=campaigns, title='important-issue')
        LandingPageFactory.create(parent=important_issue, title='overview')
        LandingPageFactory.create(parent=important_issue, title='press')
        CampaignFactory.create(parent=important_issue, title='take-action', petition=PetitionFactory.create())
        CampaignFactory.create(parent=campaigns, title='single-petition', petition=PetitionFactory.create())

        self.stdout.write('Generating LandingPage objects with known titles')
        LandingPageFactory.create(parent=opportunity, title='page')
        LandingPageFactory.create(parent=opportunity, title='page-with-signup', signup=SignupFactory.create())

        self.stdout.write('Generating LandingPage objects with known titles, and side-nav')
        side_nav = LandingPageFactory.create(parent=opportunity, title='page-side-nav')
        LandingPageFactory.create(parent=side_nav, title='sub-page')
        LandingPageFactory.create(parent=side_nav, title='sub-page-2')
        LandingPageFactory.create(parent=side_nav, title='sub-page-with-signup', signup=SignupFactory.create())

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

        try:
            home_page = Homepage.objects.get(title='Homepage')
            self.stdout.write('Homepage already exists')
        except ObjectDoesNotExist:
            self.stdout.write('Generating a Homepage')
            site_root = Page.objects.get(title='Root')
            home_page = WagtailHomepageFactory.create(
                parent=site_root,
                title='Homepage',
                slug=None,
                hero_image__file__width=1080,
                hero_image__file__height=720
            )

        try:
            default_site = Site.objects.get(is_default_site=True)
            default_site.root_page = home_page
            default_site.save()
            self.stdout.write('Updated the default Site')
        except ObjectDoesNotExist:
            self.stdout.write('Generating a default Site')
            Site.objects.create(
                hostname='localhost',
                port=8000,
                root_page=home_page,
                site_name='Foundation Home Page',
                is_default_site=True
            )

        try:
            about_page = Page.objects.get(title='about')
            self.stdout.write('about page exists')
        except ObjectDoesNotExist:
            self.stdout.write('Generating an about Page (PrimaryPage)')
            about_page = PrimaryPageFactory.create(parent=home_page, title='about')

        self.stdout.write('Generating child pages for about page')
        [PrimaryPageFactory.create(parent=about_page) for i in range(5)]

        try:
            Page.objects.get(title='styleguide')
            self.stdout.write('styleguide page exists')
        except ObjectDoesNotExist:
            self.stdout.write('Generating a Styleguide Page')
            StyleguideFactory.create(parent=home_page)

        try:
            Page.objects.get(title='people')
            self.stdout.write('people page exists')
        except ObjectDoesNotExist:
            self.stdout.write('Generating an empty People Page')
            PeoplePageFactory.create(parent=home_page)

        try:
            Page.objects.get(title='news')
            self.stdout.write('news page exists')
        except ObjectDoesNotExist:
            self.stdout.write('Generating an empty News Page')
            NewsPageFactory.create(parent=home_page)

        try:
            Page.objects.get(title='initiatives')
            self.stdout.write('initiatives page exists')
        except ObjectDoesNotExist:
            self.stdout.write('Generating an empty Initiatives Page')
            InitiativesPageFactory.create(parent=home_page)

        try:
            campaign_namespace = Page.objects.get(title='campaigns')
            self.stdout.write('campaigns namespace exists')
        except ObjectDoesNotExist:
            self.stdout.write('Generating a campaigns namespace')
            campaign_namespace = MiniSiteNameSpaceFactory.create(parent=home_page, title='campaigns', live=False)

        self.stdout.write('Generating Campaign Pages under namespace')
        [CampaignPageFactory.create(parent=campaign_namespace) for i in range(5)]

        self.stdout.write('Generating Campaigns with child pages')
        for i in range(2):
            campaign = CampaignPageFactory(parent=campaign_namespace)
            [CampaignPageFactory(parent=campaign, no_cta=True) for k in range(3)]

        try:
            opportunity_namespace = Page.objects.get(title='opportunity')
            self.stdout.write('opportunity namespace exists')
        except ObjectDoesNotExist:
            self.stdout.write('Generating an opportunity namespace')
            opportunity_namespace = MiniSiteNameSpaceFactory.create(parent=home_page, title='opportunity', live=False)

        self.stdout.write('Generating Opportunity Pages under namespace')
        [OpportunityPageFactory.create(parent=opportunity_namespace) for i in range(5)]

        self.stdout.write('Generating Opportunities with child pages')
        for i in range(2):
            opportunity = OpportunityPageFactory(parent=campaign_namespace)
            [OpportunityPageFactory(parent=opportunity, no_cta=True) for k in range(3)]

        self.stdout.write(self.style.SUCCESS('Done!'))
