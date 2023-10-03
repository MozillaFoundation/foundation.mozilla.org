from django.conf import settings
from factory import Faker, SubFactory
from wagtail.models import Page as WagtailPage
from wagtail.models import Site as WagtailSite
from wagtail_factories import PageFactory

from networkapi.donate.models import DonateHelpPage, DonateLandingPage
from networkapi.utility.faker.helpers import reseed
from networkapi.wagtailpages.factory.image_factory import ImageFactory


class DonateLandingPageFactory(PageFactory):
    class Meta:
        model = DonateLandingPage

    title = Faker("text", max_nb_chars=140)
    intro = Faker("paragraph", nb_sentences=5, variable_nb_sentences=True)
    featured_image = SubFactory(ImageFactory)


class DonateHelpPageFactory(PageFactory):
    class Meta:
        model = DonateHelpPage

    title = Faker("sentence", nb_words=2)



def generate(seed):
    reseed(seed)

    print("Generating Donate Site Landing page")
    try:
        home_page = DonateLandingPage.objects.get(title="Donate Now")
        print("Landing page already exists")
    except DonateLandingPage.DoesNotExist:
        print("Generating a Landing page")
        site_root = WagtailPage.objects.get(depth=1)

        home_page = DonateLandingPageFactory.create(parent=site_root, title="Donate Now", slug=None)

        print("Generating a Help page")
        DonateHelpPageFactory.create(parent=home_page, title="Donate Help", slug="help")

    reseed(seed)

    print("Creating Donate Site record in Wagtail")
    tds = settings.TARGET_DOMAINS
    if tds and len(tds) > 2:
        # Assume that tds[0] is the main mofo domain, and tds[1] is the Mozfest domain
        hostname = tds[2]
        port = 80
    else:
        # use a localhost domain (must be set in /etc/hosts)
        hostname = "donate.localhost"
        port = 8000

    WagtailSite.objects.create(
        hostname=hostname,
        port=port,
        root_page=home_page,
        site_name="Donate",
        is_default_site=False,
    )
