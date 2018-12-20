from django.conf import settings
from factory.django import DjangoModelFactory
from wagtail.core.models import (
    Site as WagtailSite,
    Page as WagtailPage
)
from wagtail_factories import (
    PageFactory,
    ImageFactory
)
from factory import (
    Faker,
    SubFactory,
    LazyAttribute,
    Trait
)
from networkapi.wagtailpages.models import (
    Homepage,
    Petition,
    Signup,
    PrimaryPage,
    CampaignPage,
    MiniSiteNameSpace,
    PeoplePage,
    NewsPage,
    Styleguide,
    InitiativesPage,
    ParticipatePage,
    OpportunityPage,
    HomepageFeaturedNews,
    HomepageFeaturedHighlights
)
from networkapi.wagtailpages.donation_modal import DonationModal, DonationModals
from networkapi.highlights.factory import HighlightFactory
from networkapi.news.factory import NewsFactory
from networkapi.utility.faker import StreamfieldProvider

if settings.HEROKU_APP_NAME:
    REVIEW_APP_NAME = settings.HEROKU_APP_NAME
    REVIEW_APP_HOSTNAME = f'{REVIEW_APP_NAME}.herokuapp.com'

streamfield_fields = ['header', 'paragraph', 'image', 'spacer', 'image_text2', 'quote']

Faker.add_provider(StreamfieldProvider)

sentence_faker: Faker = Faker('sentence', nb_words=3, variable_nb_words=False)
header_faker: Faker = Faker('sentence', nb_words=6, variable_nb_words=True)
description_faker: Faker = Faker('paragraphs', nb=6)


class CTAFactory(DjangoModelFactory):
    class Meta:
        abstract = True
        exclude = (
            'header_text',
            'description_text',
        )

    name = Faker('text', max_nb_chars=35)
    header = LazyAttribute(lambda o: o.header_text.rstrip('.'))
    description = LazyAttribute(lambda o: ''.join(o.description_text))
    newsletter = Faker('word')

    # Lazy Values
    description_text = description_faker
    header_text = header_faker


class PetitionFactory(CTAFactory):
    class Meta:
        model = Petition

    campaign_id = settings.PETITION_TEST_CAMPAIGN_ID


class DonationModalFactory(DjangoModelFactory):
    class Meta:
        model = DonationModal

    name = Faker('text', max_nb_chars=20)


class DonationModalsFactory(DjangoModelFactory):
    # note: plural!
    class Meta:
        model = DonationModals

    donation_modal = SubFactory(DonationModalFactory)


class SignupFactory(CTAFactory):
    class Meta:
        model = Signup


class WagtailHomepageFactory(PageFactory):
    class Meta:
        model = Homepage

    hero_headline = Faker('text', max_nb_chars=140)
    hero_story_description = Faker('paragraph', nb_sentences=5, variable_nb_sentences=True)
    hero_button_text = Faker('text', max_nb_chars=50)
    hero_button_url = Faker('url')
    hero_image = SubFactory(ImageFactory)


class CMSPageFactory(PageFactory):
    class Meta:
        abstract = True
        exclude = (
            'title_text',
            'header_text',
        )

    header = LazyAttribute(lambda o: o.header_text.rstrip('.'))
    title = LazyAttribute(lambda o: o.title_text.rstrip('.'))
    narrowed_page_content = Faker('boolean', chance_of_getting_true=50)
    body = Faker('streamfield', fields=streamfield_fields)

    # Lazy Values
    title_text = sentence_faker
    header_text = header_faker


class PrimaryPageFactory(CMSPageFactory):
    class Meta:
        model = PrimaryPage


class CampaignPageFactory(CMSPageFactory):
    class Meta:
        model = CampaignPage

    class Params:
        no_cta = Trait(cta=None)

    cta = SubFactory(PetitionFactory)


class MiniSiteNameSpaceFactory(PageFactory):
    class Meta:
        model = MiniSiteNameSpace


class PeoplePageFactory(PageFactory):
    class Meta:
        model = PeoplePage

    title = 'people'


class NewsPageFactory(PageFactory):
    class Meta:
        model = NewsPage

    title = 'news'


class StyleguideFactory(PageFactory):
    class Meta:
        model = Styleguide

    title = 'styleguide'


class InitiativesPageFactory(PageFactory):
    class Meta:
        model = InitiativesPage

    title = 'initiatives'


class ParticipatePageFactory(PageFactory):
    class Meta:
        model = ParticipatePage

    title = 'participate'


class OpportunityPageFactory(CMSPageFactory):
    class Meta:
        model = OpportunityPage

    class Params:
        no_cta = Trait(cta=None)

    cta = SubFactory(SignupFactory)


class FeaturedFactory(DjangoModelFactory):
    class Meta:
        abstract = True

    page = SubFactory(WagtailHomepageFactory)


class HomepageFeaturedNewsFactory(FeaturedFactory):
    class Meta:
        model = HomepageFeaturedNews

    news = SubFactory(NewsFactory)


class HomepageFeaturedHighlightsFactory(FeaturedFactory):
    class Meta:
        model = HomepageFeaturedHighlights

    highlight = SubFactory(HighlightFactory)


def generate():
    print('Generating blank Homepage')
    try:
        home_page = Homepage.objects.get(title='Homepage')
        print('Homepage already exists')
    except Homepage.DoesNotExist:
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
    except WagtailSite.DoesNotExist:
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
        except WagtailPage.DoesNotExist:
            print('Generating an about Page (PrimaryPage)')
            about_page = PrimaryPageFactory.create(parent=home_page, title='about')

        print('Generating child pages for about page')
        [PrimaryPageFactory.create(parent=about_page) for i in range(5)]

        try:
            WagtailPage.objects.get(title='styleguide')
            print('styleguide page exists')
        except WagtailPage.DoesNotExist:
            print('Generating a Styleguide Page')
            StyleguideFactory.create(parent=home_page)

        try:
            WagtailPage.objects.get(title='people')
            print('people page exists')
        except WagtailPage.DoesNotExist:
            print('Generating an empty People Page')
            PeoplePageFactory.create(parent=home_page)

        try:
            WagtailPage.objects.get(title='news')
            print('news page exists')
        except WagtailPage.DoesNotExist:
            print('Generating an empty News Page')
            NewsPageFactory.create(parent=home_page)

        try:
            WagtailPage.objects.get(title='initiatives')
            print('initiatives page exists')
        except WagtailPage.DoesNotExist:
            print('Generating an empty Initiatives Page')
            InitiativesPageFactory.create(parent=home_page)

        try:
            WagtailPage.objects.get(title='participate')
            print('participate page exists')
        except WagtailPage.DoesNotExist:
            print('Generating an empty Participate Page')
            ParticipatePageFactory.create(parent=home_page)

        try:
            campaign_namespace = WagtailPage.objects.get(title='campaigns')
            print('campaigns namespace exists')
        except WagtailPage.DoesNotExist:
            print('Generating a campaigns namespace')
            campaign_namespace = MiniSiteNameSpaceFactory.create(parent=home_page, title='campaigns', live=False)

        print('Generating Campaign Pages under namespace')
        campaigns = [CampaignPageFactory.create(parent=campaign_namespace) for i in range(5)]

        print('Generating Donation Modals for Campaign Pages')
        [DonationModalsFactory.create(page=campaign) for campaign in campaigns]

        try:
            CampaignPage.objects.get(title='single-page')
            print('single-page CampaignPage already exists')
        except CampaignPage.DoesNotExist:
            print('Generating single-page CampaignPage')
            CampaignPageFactory.create(parent=campaign_namespace, title='single-page')

        try:
            CampaignPage.objects.get(title='multi-page')
            print('multi-page CampaignPage already exists.')
        except CampaignPage.DoesNotExist:
            print('Generating multi-page CampaignPage')
            multi_page_campaign = CampaignPageFactory(parent=campaign_namespace, title='multi-page')
            [CampaignPageFactory(parent=multi_page_campaign, no_cta=True) for k in range(3)]

        try:
            opportunity_namespace = WagtailPage.objects.get(title='opportunity')
            print('opportunity namespace exists')
        except WagtailPage.DoesNotExist:
            print('Generating an opportunity namespace')
            opportunity_namespace = MiniSiteNameSpaceFactory.create(parent=home_page, title='opportunity', live=False)

        print('Generating Opportunity Pages under namespace')
        [OpportunityPageFactory.create(parent=opportunity_namespace) for i in range(5)]

        try:
            OpportunityPage.objects.get(title='Global Sprint')
            print('Global Sprint OpportunityPage exists')
        except OpportunityPage.DoesNotExist:
            print('Generating Global Sprint OpportunityPage')
            OpportunityPageFactory.create(parent=opportunity_namespace, title='Global Sprint', no_cta=True)

        try:
            OpportunityPage.objects.get(title='single-page')
            print('single-page OpportunityPage exists')
        except OpportunityPage.DoesNotExist:
            print('Generating single-page OpportunityPage')
            OpportunityPageFactory.create(parent=opportunity_namespace, title='single-page')

        try:
            OpportunityPage.objects.get(title='multi-page')
            print('multi-page OpportunityPage exists')
        except OpportunityPage.DoesNotExist:
            print('Generating multi-page OpportunityPage')
            multi_page_opportunity = OpportunityPageFactory(parent=opportunity_namespace, title='multi-page')
            [OpportunityPageFactory(parent=multi_page_opportunity, no_cta=True) for k in range(3)]
