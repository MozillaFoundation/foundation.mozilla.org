from itertools import chain, combinations

import factory
from random import randint, random

from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings

from networkapi.people.models import InternetHealthIssue

from wagtail.core.models import (
    Site as WagtailSite,
    Page as WagtailPage
)

# Factories
from networkapi.highlights.factory import HighlightFactory
from networkapi.milestones.factory import MilestoneFactory
from networkapi.news.factory import NewsFactory
from networkapi.people.factory import (
    PersonFactory,
    AffiliationFactory,
)
from networkapi.wagtailpages.factory import (
    WagtailHomepageFactory,
    PrimaryPageFactory,
    OpportunityPageFactory,
    StyleguideFactory,
    PeoplePageFactory,
    NewsPageFactory,
    InitiativesPageFactory,
    MiniSiteNameSpaceFactory,
    CampaignPageFactory,
    HomepageFeaturedNewsFactory,
    HomepageFeaturedHighlightsFactory,
    ParticipatePageFactory,
    DonationModalsFactory,
)

from networkapi.buyersguide.models import (
    Product,
    RangeVote,
    BooleanVote
)
from networkapi.buyersguide.factory import ProductFactory

# Wagtail Page Models
import networkapi.wagtailpages.models as wagtailpages_models

internet_health_issues = [
    'Digital Inclusion',
    'Web Literacy',
    'Open Innovation',
    'Decentralization',
    'Online Privacy and Security',
]

if settings.HEROKU_APP_NAME:
    REVIEW_APP_NAME = settings.HEROKU_APP_NAME
    REVIEW_APP_HOSTNAME = f'{REVIEW_APP_NAME}.herokuapp.com'


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
        else:
            seed = randint(0, 5000000)

        print('Seeding Faker with: {}'.format(seed))
        faker = factory.faker.Faker._get_faker(locale='en-US')
        faker.random.seed(seed)

        print('Generating Milestones')
        [MilestoneFactory.create() for i in range(10)]

        print('Generating five InternetHealthIssue')
        [InternetHealthIssue.objects.get_or_create(name=e) for e in internet_health_issues]

        print('Generating Fake News')
        generate_fake_data(NewsFactory, 10)

        print('Generating highlights')
        generate_fake_data(HighlightFactory, 4)

        print('Generating People')
        generate_fake_data(PersonFactory, 10)

        print('Generating People with affiliation')
        generate_fake_data(AffiliationFactory, 10)

        print('Generating blank Homepage')
        try:
            home_page = wagtailpages_models.Homepage.objects.get(title='Homepage')
            print('Homepage already exists')
        except ObjectDoesNotExist:
            print('Generating a Homepage')
            site_root = WagtailPage.objects.get(title='Root')
            home_page = WagtailHomepageFactory.create(
                parent=site_root,
                title='Homepage',
                slug=None,
                hero_image__file__width=1080,
                hero_image__file__height=720
            )

        print('Generating Homepage Highlights and News')
        featured_news = [NewsFactory.create() for i in range(6)]
        featured_highlights = [HighlightFactory.create() for i in range(6)]
        home_page.featured_news = [
            HomepageFeaturedNewsFactory.build(news=featured_news[i]) for i in range(6)
        ]
        home_page.featured_highlights = [
            HomepageFeaturedHighlightsFactory.build(highlight=featured_highlights[i]) for i in range(6)
        ]
        home_page.save()

        try:
            default_site = WagtailSite.objects.get(is_default_site=True)
            if settings.HEROKU_APP_NAME:
                default_site.hostname = REVIEW_APP_HOSTNAME
            default_site.root_page = home_page
            default_site.save()
            print('Updated the default Site')
        except ObjectDoesNotExist:
            print('Generating a default Site')
            if settings.HEROKU_APP_NAME:
                hostname = REVIEW_APP_HOSTNAME
                port = 80
            else:
                hostname = 'localhost'
                port = 8000

            WagtailSite.objects.create(
                hostname=hostname,
                port=port,
                root_page=home_page,
                site_name='Foundation Home Page',
                is_default_site=True
            )

        try:
            about_page = WagtailPage.objects.get(title='about')
            print('about page exists')
        except ObjectDoesNotExist:
            print('Generating an about Page (PrimaryPage)')
            about_page = PrimaryPageFactory.create(parent=home_page, title='about')

        print('Generating child pages for about page')
        [PrimaryPageFactory.create(parent=about_page) for i in range(5)]

        try:
            WagtailPage.objects.get(title='styleguide')
            print('styleguide page exists')
        except ObjectDoesNotExist:
            print('Generating a Styleguide Page')
            StyleguideFactory.create(parent=home_page)

        try:
            WagtailPage.objects.get(title='people')
            print('people page exists')
        except ObjectDoesNotExist:
            print('Generating an empty People Page')
            PeoplePageFactory.create(parent=home_page)

        try:
            WagtailPage.objects.get(title='news')
            print('news page exists')
        except ObjectDoesNotExist:
            print('Generating an empty News Page')
            NewsPageFactory.create(parent=home_page)

        try:
            WagtailPage.objects.get(title='initiatives')
            print('initiatives page exists')
        except ObjectDoesNotExist:
            print('Generating an empty Initiatives Page')
            InitiativesPageFactory.create(parent=home_page)

        try:
            WagtailPage.objects.get(title='participate')
            print('participate page exists')
        except ObjectDoesNotExist:
            print('Generating an empty Participate Page')
            ParticipatePageFactory.create(parent=home_page)

        try:
            campaign_namespace = WagtailPage.objects.get(title='campaigns')
            print('campaigns namespace exists')
        except ObjectDoesNotExist:
            print('Generating a campaigns namespace')
            campaign_namespace = MiniSiteNameSpaceFactory.create(parent=home_page, title='campaigns', live=False)

        print('Generating Campaign Pages under namespace')
        campaigns = [CampaignPageFactory.create(parent=campaign_namespace) for i in range(5)]

        print('Generating Donation Modals for Campaign Pages')
        [DonationModalsFactory.create(page=campaign) for campaign in campaigns]

        try:
            wagtailpages_models.CampaignPage.objects.get(title='single-page')
            print('single-page CampaignPage already exists')
        except ObjectDoesNotExist:
            print('Generating single-page CampaignPage')
            CampaignPageFactory.create(parent=campaign_namespace, title='single-page')

        try:
            wagtailpages_models.CampaignPage.objects.get(title='multi-page')
            print('multi-page CampaignPage already exists.')
        except ObjectDoesNotExist:
            print('Generating multi-page CampaignPage')
            multi_page_campaign = CampaignPageFactory(parent=campaign_namespace, title='multi-page')
            [CampaignPageFactory(parent=multi_page_campaign, no_cta=True) for k in range(3)]

        try:
            opportunity_namespace = WagtailPage.objects.get(title='opportunity')
            print('opportunity namespace exists')
        except ObjectDoesNotExist:
            print('Generating an opportunity namespace')
            opportunity_namespace = MiniSiteNameSpaceFactory.create(parent=home_page, title='opportunity', live=False)

        print('Generating Opportunity Pages under namespace')
        [OpportunityPageFactory.create(parent=opportunity_namespace) for i in range(5)]

        try:
            wagtailpages_models.OpportunityPage.objects.get(title='Global Sprint')
            print('Global Sprint OpportunityPage exists')
        except ObjectDoesNotExist:
            print('Generating Global Sprint OpportunityPage')
            OpportunityPageFactory.create(parent=opportunity_namespace, title='Global Sprint', no_cta=True)

        try:
            wagtailpages_models.OpportunityPage.objects.get(title='single-page')
            print('single-page OpportunityPage exists')
        except ObjectDoesNotExist:
            print('Generating single-page OpportunityPage')
            OpportunityPageFactory.create(parent=opportunity_namespace, title='single-page')

        try:
            wagtailpages_models.OpportunityPage.objects.get(title='multi-page')
            print('multi-page OpportunityPage exists')
        except ObjectDoesNotExist:
            print('Generating multi-page OpportunityPage')
            multi_page_opportunity = OpportunityPageFactory(parent=opportunity_namespace, title='multi-page')
            [OpportunityPageFactory(parent=multi_page_opportunity, no_cta=True) for k in range(3)]

        print('Generating Buyer\'s Guide Products')
        generate_fake_data(ProductFactory, 70)

        print('Generating Randomised Buyer\'s Guide Products Votes')
        for p in Product.objects.all():
            for _ in range(1, 15):
                value = randint(1, 100)
                RangeVote.objects.create(
                    product=p,
                    attribute='creepiness',
                    value=value
                )

                value = (random() < 0.5)
                BooleanVote.objects.create(
                    product=p,
                    attribute='confidence',
                    value=value
                )

        print('Aggregating Buyer\'s Guide Product votes')
        call_command('aggregate_product_votes')

        print(self.style.SUCCESS('Done!'))
