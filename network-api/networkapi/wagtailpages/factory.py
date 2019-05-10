from django.conf import settings
from datetime import timezone
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
from networkapi.utility.faker.helpers import reseed

RANDOM_SEED = settings.RANDOM_SEED
TESTING = settings.TESTING

if settings.HEROKU_APP_NAME:
    REVIEW_APP_NAME = settings.HEROKU_APP_NAME
    REVIEW_APP_HOSTNAME = f'{REVIEW_APP_NAME}.herokuapp.com'

streamfield_fields = ['header', 'paragraph', 'image', 'spacer', 'image_text2', 'quote']
blog_body_streamfield_fields = ['paragraph', 'image', 'image_text', 'image_text_mini',
                                'video', 'linkbutton', 'spacer', 'quote']

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


class ParticipatePage2Factory(PageFactory):
    class Meta:
        model = networkapi.wagtailpages.models.ParticipatePage2

    title = 'participate'
    h2 = Faker('text', max_nb_chars=20)
    h2Subheader = Faker('text', max_nb_chars=250)

    # first block
    ctaHero = SubFactory(ImageFactory)
    ctaHeroHeader = Faker('text', max_nb_chars=50)
    ctaCommitment = Faker('text', max_nb_chars=10)
    ctaButtonTitle = Faker('text', max_nb_chars=50)
    ctaButtonURL = Faker('url')

    # second block
    ctaHero2 = SubFactory(ImageFactory)
    ctaHeroHeader2 = Faker('text', max_nb_chars=50)
    ctaCommitment2 = Faker('text', max_nb_chars=10)
    ctaButtonTitle2 = Faker('text', max_nb_chars=50)
    ctaButtonURL2 = Faker('url')

    # third block
    ctaHero3 = SubFactory(ImageFactory)
    ctaHeroHeader3 = Faker('text', max_nb_chars=50)
    ctaHeroSubhead3 = Faker('paragraph', nb_sentences=5, variable_nb_sentences=True)
    ctaCommitment3 = Faker('text', max_nb_chars=10)
    ctaFacebook3 = Faker('text', max_nb_chars=20)
    ctaTwitter3 = Faker('text', max_nb_chars=20)
    ctaEmailShareBody3 = Faker('text', max_nb_chars=20)
    ctaEmailShareSubject3 = Faker('text', max_nb_chars=50)

    # TODO: reduce all this duplication


class ParticipateFeaturedFactory(DjangoModelFactory):
    class Meta:
        abstract = True

    page = SubFactory(ParticipatePage2Factory)


class ParticipatePage2FeaturedHighlightsFactory(ParticipateFeaturedFactory):
    class Meta:
        model = networkapi.wagtailpages.models.ParticipateHighlights

    highlight = SubFactory(HighlightFactory)


class ParticipatePage2FeaturedHighlights2Factory(ParticipateFeaturedFactory):
    class Meta:
        model = networkapi.wagtailpages.models.ParticipateHighlights2

    highlight = SubFactory(HighlightFactory)


class OpportunityPageFactory(CMSPageFactory):
    class Meta:
        model = OpportunityPage


class BlogPageFactory(PageFactory):

    class Meta:
        model = networkapi.wagtailpages.models.BlogPage
        exclude = (
            'title_text',
        )

    title = LazyAttribute(lambda o: o.title_text.rstrip('.'))
    author = Faker('name')
    body = Faker('streamfield', fields=blog_body_streamfield_fields)
    first_published_at = (Faker('date_time', tzinfo=timezone.utc) if RANDOM_SEED and not TESTING
                          else Faker('past_datetime', start_date='-30d', tzinfo=timezone.utc))
    live = True

    # Lazy Values
    title_text = sentence_faker


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


def generate(seed):
    reseed(seed)
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

    reseed(seed)
    
    print('Generating Homepage Highlights and News')
    if home_page is not None:
        featured_news = [NewsFactory.create() for i in range(6)]
        featured_highlights = [HighlightFactory.create() for i in range(6)]
        home_page.featured_news = [
            HomepageFeaturedNewsFactory.build(news=featured_news[i]) for i in range(6)
        ]
        home_page.featured_highlights = [
            HomepageFeaturedHighlightsFactory.build(highlight=featured_highlights[i]) for i in range(6)
        ]
        home_page.save()

    reseed(seed)

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

        reseed(seed)

        try:
            about_page = WagtailPage.objects.get(title='about')
            print('about page exists')
        except WagtailPage.DoesNotExist:
            print('Generating an about Page (PrimaryPage)')
            about_page = PrimaryPageFactory.create(parent=home_page, title='about')

        reseed(seed)

        print('Generating child pages for about page')
        [PrimaryPageFactory.create(parent=about_page) for i in range(5)]

        try:
            WagtailPage.objects.get(title='styleguide')
            print('styleguide page exists')
        except WagtailPage.DoesNotExist:
            print('Generating a Styleguide Page')
            StyleguideFactory.create(parent=home_page)

        reseed(seed)

        try:
            WagtailPage.objects.get(title='people')
            print('people page exists')
        except WagtailPage.DoesNotExist:
            print('Generating an empty People Page')
            PeoplePageFactory.create(parent=home_page)

        reseed(seed)

        try:
            WagtailPage.objects.get(title='news')
            print('news page exists')
        except WagtailPage.DoesNotExist:
            print('Generating an empty News Page')
            NewsPageFactory.create(parent=home_page)

        reseed(seed)

        try:
            WagtailPage.objects.get(title='initiatives')
            print('initiatives page exists')
        except WagtailPage.DoesNotExist:
            print('Generating an empty Initiatives Page')
            InitiativesPageFactory.create(parent=home_page)

        reseed(seed)

        try:
            participate_page = WagtailPage.objects.get(title='participate')
            print('participate page exists')
        except WagtailPage.DoesNotExist:
            print('Generating an empty Participate Page')
            participate_page = ParticipatePage2Factory.create(parent=home_page)

        reseed(seed)

        print('Generating Participate Highlights')
        if participate_page is not None:
            featured_highlights = [HighlightFactory.create() for i in range(3)]
            participate_page.featured_highlights = [
                ParticipatePage2FeaturedHighlightsFactory.build(highlight=featured_highlights[i]) for i in range(3)
            ]
            featured_highlights2 = [HighlightFactory.create() for i in range(6)]
            participate_page.featured_highlights2 = [
                ParticipatePage2FeaturedHighlights2Factory.build(highlight=featured_highlights2[i]) for i in range(6)
            ]
            participate_page.save()

        reseed()

        try:
            campaign_namespace = WagtailPage.objects.get(title='campaigns')
            print('campaigns namespace exists')
        except WagtailPage.DoesNotExist:
            print('Generating a campaigns namespace')
            campaign_namespace = MiniSiteNameSpaceFactory.create(parent=home_page, title='campaigns', live=False)

        reseed(seed)

        print('Generating Campaign Pages under namespace')
        campaigns = [CampaignPageFactory.create(parent=campaign_namespace) for i in range(5)]

        reseed(seed)

        print('Generating Donation Modals for Campaign Pages')
        [DonationModalsFactory.create(page=campaign) for campaign in campaigns]

        reseed(seed)

        try:
            CampaignPage.objects.get(title='single-page')
            print('single-page CampaignPage already exists')
        except CampaignPage.DoesNotExist:
            print('Generating single-page CampaignPage')
            CampaignPageFactory.create(parent=campaign_namespace, title='single-page')

        reseed(seed)

        try:
            CampaignPage.objects.get(title='multi-page')
            print('multi-page CampaignPage already exists.')
        except CampaignPage.DoesNotExist:
            print('Generating multi-page CampaignPage')
            multi_page_campaign = CampaignPageFactory(parent=campaign_namespace, title='multi-page')
            [CampaignPageFactory(parent=multi_page_campaign, no_cta=True) for k in range(3)]

        reseed(seed)

        try:
            opportunity_namespace = WagtailPage.objects.get(title='opportunity')
            print('opportunity namespace exists')
        except WagtailPage.DoesNotExist:
            print('Generating an opportunity namespace')
            opportunity_namespace = MiniSiteNameSpaceFactory.create(parent=home_page, title='opportunity', live=False)

        reseed(seed)

        print('Generating Opportunity Pages under namespace')
        [OpportunityPageFactory.create(parent=opportunity_namespace) for i in range(5)]

        reseed(seed)

        try:
            OpportunityPage.objects.get(title='Global Sprint')
            print('Global Sprint OpportunityPage exists')
        except OpportunityPage.DoesNotExist:
            print('Generating Global Sprint OpportunityPage')
            OpportunityPageFactory.create(parent=opportunity_namespace, title='Global Sprint', no_cta=True)

        reseed(seed)

        try:
            OpportunityPage.objects.get(title='single-page')
            print('single-page OpportunityPage exists')
        except OpportunityPage.DoesNotExist:
            print('Generating single-page OpportunityPage')
            OpportunityPageFactory.create(parent=opportunity_namespace, title='single-page')

        reseed(seed)

        try:
            OpportunityPage.objects.get(title='multi-page')
            print('multi-page OpportunityPage exists')
        except OpportunityPage.DoesNotExist:
            print('Generating multi-page OpportunityPage')
            multi_page_opportunity = OpportunityPageFactory(parent=opportunity_namespace, title='multi-page')
            [OpportunityPageFactory(parent=multi_page_opportunity, no_cta=True) for k in range(3)]

        reseed(seed)]

        try:
            blog_namespace = WagtailPage.objects.get(title='blog')
            print('blog namespace exists')
        except WagtailPage.DoesNotExist:
            print('Generating a blog namespace')
            blog_namespace = MiniSiteNameSpaceFactory.create(parent=home_page, title='blog', live=False)

        print('Generating Blog Pages under namespace')
        [BlogPageFactory.create(parent=blog_namespace) for i in range(3)]

        reseed(seed)

