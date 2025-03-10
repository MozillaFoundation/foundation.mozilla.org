from django.conf import settings
from factory import Faker, SubFactory
from wagtail.images.models import Image
from wagtail.models import Page as WagtailPage
from wagtail.models import Site as WagtailSite
from wagtail_factories import PageFactory

from foundation_cms.legacy_apps.utility.faker.helpers import get_homepage, reseed
from foundation_cms.legacy_apps.wagtailpages.factory.image_factory import ImageFactory
from foundation_cms.legacy_apps.wagtailpages.models import FocusArea, Homepage

from .primary_page import PrimaryPageFactory

if settings.HEROKU_APP_NAME:
    REVIEW_APP_NAME = settings.HEROKU_APP_NAME
    REVIEW_APP_HOSTNAME = f"{REVIEW_APP_NAME}.herokuapp.com"


class WagtailHomepageFactory(PageFactory):
    class Meta:
        model = Homepage

    hero_headline = Faker("text", max_nb_chars=80)
    hero_button_text = Faker("text", max_nb_chars=50)
    hero_button_url = Faker("url")
    hero_image = SubFactory(ImageFactory)
    cause_statement = Faker("text", max_nb_chars=150)
    # cause_statement_link_text and cause_statement_link_page are created at a later state
    hero_intro_heading = Faker("text", max_nb_chars=60)
    hero_intro_body = Faker("text", max_nb_chars=250)
    hero_intro_link = Faker("streamfield", fields=["homepage_hero_intro_link"])
    quote_image = SubFactory(ImageFactory)
    quote_text = Faker("text", max_nb_chars=300)
    quote_source_name = Faker("text", max_nb_chars=30)
    quote_source_job_title = Faker("text", max_nb_chars=50)
    partner_background_image = SubFactory(ImageFactory)
    partner_intro_text = Faker("text", max_nb_chars=80)
    ideas_headline = Faker("text", max_nb_chars=100)
    ideas_image = SubFactory(ImageFactory)


def generate(seed):
    reseed(seed)

    print("Generating blank Homepage")
    try:
        home_page = get_homepage()
        print("Homepage already exists")
    except Homepage.DoesNotExist:
        print("Generating a Homepage")
        site_root = WagtailPage.objects.get(id=1)
        home_page = WagtailHomepageFactory.create(
            parent=site_root,
            title="Homepage",
            slug=None,
            hero_image__file__width=1080,
            hero_image__file__height=720,
        )

    reseed(seed)

    print("Creating a legacy site record in Wagtail")
    tds = settings.TARGET_DOMAINS
    if tds and len(tds) > 1:
        # Assume that tds[0] is the main mofo domain, and tds[1] is the legacy domain
        hostname = tds[1]
        port = 80
    else:
        # use a localhost domain (must be set in /etc/hosts)
        hostname = "legacy.localhost"
        port = 8000

    WagtailSite.objects.create(
        hostname=hostname,
        port=port,
        root_page=home_page,
        site_name="Legacy Site",
        is_default_site=False,
    )

    reseed(seed)

    print("Assigning images to areas of focus")
    for area in FocusArea.objects.all():
        area.interest_icon = Image.objects.first()
        area.save()

    reseed(seed)

    try:
        wwa_page = WagtailPage.objects.get(title="Who we are")
        print('"who we are" page exists')
    except WagtailPage.DoesNotExist:
        print('Generating "who we are" Page (PrimaryPage)')
        wwa_page = PrimaryPageFactory.create(parent=home_page, title="Who we are", show_in_menus=True)

    home_page.save()

    reseed(seed)

    print('Generating child pages for "who we are" page')
    [PrimaryPageFactory.create(parent=wwa_page) for i in range(5)]

    reseed(seed)

    try:
        WagtailPage.objects.get(title="What we do")
        print('"what we do" page exists')
    except WagtailPage.DoesNotExist:
        print('Generating "what we do" Page (PrimaryPage)')
        PrimaryPageFactory.create(parent=home_page, title="What we do", show_in_menus=True)
