import random

from django.conf import settings
from factory import Faker, LazyAttribute, SubFactory
from factory.django import DjangoModelFactory
from wagtail.models import Page as WagtailPage
from wagtail.models import Site as WagtailSite
from wagtail_factories import PageFactory

from networkapi.mozfest import models as mozfest_models
from networkapi.utility.faker import StreamfieldProvider
from networkapi.utility.faker.helpers import reseed
from networkapi.wagtailpages.factory.image_factory import ImageFactory
from networkapi.wagtailpages.factory.signup import SignupFactory

streamfield_fields = [
    "paragraph",
    "image",
    "spacer",
    "quote",
    "carousel_and_text",
    "statistics",
    "listing",
    "carousel_text_block",
    "stats_block",
    "dark_quote",
    "listing",
    "tickets_block",
]


Faker.add_provider(StreamfieldProvider)

is_review_app = False
if settings.HEROKU_APP_NAME:
    is_review_app = True


class MozfestPrimaryPageFactory(PageFactory):
    class Meta:
        model = mozfest_models.MozfestPrimaryPage
        exclude = "header_text"

    header = LazyAttribute(lambda o: o.header_text.rstrip("."))
    banner = SubFactory(ImageFactory)
    intro = Faker("paragraph", nb_sentences=3, variable_nb_sentences=False)
    body = Faker("streamfield", fields=streamfield_fields)
    header_text = Faker("sentence", nb_words=6, variable_nb_words=True)


class MozfestHomepageFactory(MozfestPrimaryPageFactory):
    class Meta:
        model = mozfest_models.MozfestHomepage
        exclude = ("header_text", "banner_heading_text")

    banner_heading = Faker("sentence", nb_words=6, variable_nb_words=True)
    banner_meta = "1st–3rd June 2024 | MALDIVES"
    banner_text = Faker("sentence", nb_words=12, variable_nb_words=True)
    banner_link_url = Faker("url")
    banner_link_text = Faker("sentence", nb_words=2, variable_nb_words=True)

    body = Faker("streamfield", fields=streamfield_fields + ["current_events_slider"])

    signup = SubFactory(SignupFactory)


class MozfestLandingPageFactory(PageFactory):
    class Meta:
        model = mozfest_models.MozfestLandingPage

    body = Faker("streamfield", fields=streamfield_fields)
    banner = SubFactory(ImageFactory)
    banner_heading = Faker("sentence", nb_words=6, variable_nb_words=True)
    banner_meta = "1st–3rd June 2024 | MALDIVES"
    banner_text = Faker("sentence", nb_words=12, variable_nb_words=True)
    banner_link_url = Faker("url")
    banner_link_text = Faker("sentence", nb_words=2, variable_nb_words=True)


class TicketSnippetFactory(DjangoModelFactory):
    class Meta:
        model = mozfest_models.Ticket

    name = Faker("sentence", nb_words=2)
    cost = f"€{random.choice(['100', '200', '300'])}"
    group = Faker("text", max_nb_chars=50)
    description = Faker("text", max_nb_chars=250)
    link_text = Faker("text", max_nb_chars=25)
    link_url = Faker("url")
    sticker_text = Faker("text", max_nb_chars=25)


def generate(seed):
    reseed(seed)

    print("Generating Mozfest Homepage")
    try:
        home_page = mozfest_models.MozfestHomepage.objects.get(title="Mozilla Festival")
        print("Homepage already exists")
    except mozfest_models.MozfestHomepage.DoesNotExist:
        print("Generating a Homepage")
        site_root = WagtailPage.objects.get(depth=1)

        home_page = MozfestHomepageFactory.create(parent=site_root, title="Mozilla Festival", slug=None)

    reseed(seed)

    print("Creating MozFest Site record in Wagtail")
    tds = settings.TARGET_DOMAINS
    if tds and len(tds) > 1:
        # Assume that tds[0] is the main mofo domain, and tds[1] is the Mozfest domain
        hostname = tds[1]
        port = 80
    else:
        # use a localhost domain (must be set in /etc/hosts)
        hostname = "mozfest.localhost"
        port = 8000

    WagtailSite.objects.create(
        hostname=hostname,
        port=port,
        root_page=home_page,
        site_name="Mozilla Festival",
        is_default_site=False,
    )

    print("Generating Mozfest sub-pages")
    [
        MozfestPrimaryPageFactory.create(parent=home_page, title=title)
        for title in ["Spaces", "Tickets", "Team", "Sponsors"]
    ]

    print("Generating Mozfest landing-pages")
    [MozfestLandingPageFactory.create(parent=home_page, title=title) for title in ["Landing page 1", "Landing page 2"]]
