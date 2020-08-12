from factory import (
    DjangoModelFactory,
    Faker,
    SubFactory,
)
from wagtail_factories import ImageFactory

from wagtail.core.models import Page

from networkapi.utility.faker import generate_fake_data
from networkapi.utility.faker.helpers import reseed
from networkapi.wagtailpages.models import FocusArea


class FocusAreaFactory(DjangoModelFactory):
    class Meta:
        model = FocusArea

    interest_icon = SubFactory(ImageFactory)
    name = Faker('text', max_nb_chars=100)
    description = Faker('text', max_nb_chars=300)
    page = Page.objects.order_by("?").first()


def generate(seed):
    reseed(seed)

    print('Generating Areas of Focus')
    generate_fake_data(FocusAreaFactory, 7)
