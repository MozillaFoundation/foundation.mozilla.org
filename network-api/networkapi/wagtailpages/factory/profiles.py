from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from networkapi.utility.faker import generate_fake_data
from networkapi.utility.faker.helpers import reseed
from networkapi.wagtailpages.models import Profile
from networkapi.wagtailpages.factory import image_factory

NUM_PROFILES = 10


class ProfileFactory(DjangoModelFactory):

    class Meta:
        model = Profile

    name = Faker('name')
    tagline = Faker('text', max_nb_chars=50)
    introduction = Faker('paragraph')
    image = SubFactory(image_factory.ImageFactory)


def generate(seed):
    reseed(seed)

    print('Generating profiles')
    generate_fake_data(ProfileFactory, NUM_PROFILES)
