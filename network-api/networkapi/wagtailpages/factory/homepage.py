from django.conf import settings
from factory import (
    Faker,
    SubFactory
)
from wagtail_factories import (
    PageFactory,
    ImageFactory
)
from wagtail.core.models import (
    Site as WagtailSite,
    Page as WagtailPage
)

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

    hero_headline = Faker('text', max_nb_chars=140)
    hero_story_description = Faker('paragraph', nb_sentences=5, variable_nb_sentences=True)
    hero_button_text = Faker('text', max_nb_chars=25)
    hero_button_url = Faker('url')
    hero_image = SubFactory(ImageFactory)


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
