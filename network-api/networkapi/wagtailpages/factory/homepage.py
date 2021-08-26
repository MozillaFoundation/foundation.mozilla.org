from django.conf import settings
from factory import (
    Faker,
    SubFactory
)
from wagtail_factories import PageFactory
from wagtail.core.models import (
    Site as WagtailSite,
    Page as WagtailPage
)
from networkapi.wagtailpages.factory.image_factory import ImageFactory
from networkapi.wagtailpages.models import Homepage
from networkapi.utility.faker.helpers import (
    reseed,
    get_homepage
)
from .primary_page import PrimaryPageFactory

if settings.HEROKU_APP_NAME:
    REVIEW_APP_NAME = settings.HEROKU_APP_NAME
    REVIEW_APP_HOSTNAME = f'{REVIEW_APP_NAME}.herokuapp.com'


class WagtailHomepageFactory(PageFactory):
    class Meta:
        model = Homepage

    hero_headline = Faker('text', max_nb_chars=80)
    hero_button_text = Faker('text', max_nb_chars=50)
    hero_button_url = Faker('url')
    hero_image = SubFactory(ImageFactory)
    cause_statement = Faker('text', max_nb_chars=150)
    # cause_statement_link_text and cause_statement_link_page are created at a later state
    quote_image = SubFactory(ImageFactory)
    quote_text = Faker('text', max_nb_chars=300)
    quote_source_name = Faker('text', max_nb_chars=30)
    quote_source_job_title = Faker('text', max_nb_chars=50)
    partner_background_image = SubFactory(ImageFactory)
    partner_intro_text = Faker('text', max_nb_chars=80)
    spotlight_headline = Faker('text', max_nb_chars=100)
    spotlight_image = SubFactory(ImageFactory)


def generate(seed):
    reseed(seed)

    print('Generating blank Homepage')
    try:
        home_page = get_homepage()
        print('Homepage already exists')
    except Homepage.DoesNotExist:
        print('Generating a Homepage')
        site_root = WagtailPage.objects.get(id=1)
        home_page = WagtailHomepageFactory.create(
            parent=site_root,
            title='Homepage',
            slug=None,
            hero_image__file__width=1080,
            hero_image__file__height=720
        )

    reseed(seed)

    try:
        default_site = WagtailSite.objects.get(is_default_site=True)
        default_site.root_page = home_page
        if settings.HEROKU_APP_NAME:
            hostname = REVIEW_APP_HOSTNAME
            port = 80
        else:
            hostname = 'localhost'
            port = 8000
        default_site.hostname = hostname
        default_site.port = port
        default_site.site_name = "Foundation Home Page"
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
        wwa_page = WagtailPage.objects.get(title='Who we are')
        print('"who we are" page exists')
    except WagtailPage.DoesNotExist:
        print('Generating "who we are" Page (PrimaryPage)')
        wwa_page = PrimaryPageFactory.create(
            parent=home_page,
            title='Who we are',
            show_in_menus=True
        )

    reseed(seed)

    print('Generating child pages for "who we are" page')
    [PrimaryPageFactory.create(parent=wwa_page) for i in range(5)]

    reseed(seed)

    try:
        WagtailPage.objects.get(title='What we do')
        print('"what we do" page exists')
    except WagtailPage.DoesNotExist:
        print('Generating "what we do" Page (PrimaryPage)')
        PrimaryPageFactory.create(
            parent=home_page,
            title='What we do',
            show_in_menus=True
        )
