from django.conf import settings
from factory import Faker, SubFactory
from wagtail_factories import PageFactory

from legacy_cms.donate.models import DonateLandingPage
from legacy_cms.utility.faker import StreamfieldProvider
from legacy_cms.utility.faker.helpers import reseed
from legacy_cms.wagtailpages.factory.image_factory import ImageFactory
from legacy_cms.wagtailpages.models import Homepage

description_faker = Faker("paragraphs", nb=2)


Faker.add_provider(StreamfieldProvider)

streamfield_fields = ["paragraph", "spacer", "image", "image_text", "quote"]


class DonateLandingPageFactory(PageFactory):
    class Meta:
        model = DonateLandingPage

    title = Faker("text", max_nb_chars=140)
    intro = Faker("paragraph", nb_sentences=5, variable_nb_sentences=True)
    featured_image = SubFactory(ImageFactory)


def generate(seed):
    reseed(seed)

    print("Generating Donate Site Landing page")
    try:
        DonateLandingPage.objects.get(title="Donate Now")
        print("Landing page already exists")
    except DonateLandingPage.DoesNotExist:
        print("Generating a Landing page")
        homepage = Homepage.objects.get(locale__language_code=settings.LANGUAGE_CODE)
        DonateLandingPageFactory.create(parent=homepage, title="Donate Now", slug="donate")
