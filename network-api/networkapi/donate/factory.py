import wagtail_factories
from django.conf import settings
from factory import Faker, LazyAttribute, SubFactory
from wagtail.models import Page as WagtailPage
from wagtail.models import Site as WagtailSite
from wagtail_factories import PageFactory

from networkapi.donate.models import DonateHelpPage, DonateLandingPage
from networkapi.donate.pagemodels.customblocks.notice_block import NoticeBlock
from networkapi.utility.faker import StreamfieldProvider
from networkapi.utility.faker.helpers import reseed
from networkapi.wagtailpages.factory.image_factory import ImageFactory

description_faker: Faker = Faker("paragraphs", nb=2)


Faker.add_provider(StreamfieldProvider)

streamfield_fields = ["paragraph", "spacer", "image", "image_text", "quote"]


class NoticeBlockFactory(wagtail_factories.StructBlockFactory):
    class Meta:
        model = NoticeBlock
        exclude = ("description_text",)

    image = SubFactory(wagtail_factories.ImageChooserBlockFactory)
    image_alt_text = Faker("sentence", nb_words=4)
    text = LazyAttribute(lambda o: "".join([f"<p>{p}</p>" for p in o.description_text]))

    # Lazy Values
    description_text = description_faker


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
    body = Faker("streamfield", fields=streamfield_fields)
    notice = wagtail_factories.StreamFieldFactory({"notice": SubFactory(NoticeBlockFactory)})


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
        DonateHelpPageFactory(parent=home_page, title="Donate Help", slug="help", notice__0="notice")

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
