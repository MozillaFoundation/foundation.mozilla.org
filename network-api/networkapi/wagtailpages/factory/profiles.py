from factory import Faker
from factory.django import DjangoModelFactory

from networkapi.wagtailpages.models import Profile
from networkapi.utility.faker import generate_fake_data
from networkapi.utility.faker.helpers import reseed

NUM_PROFILES = 10


class ProfileFactory(DjangoModelFactory):

    class Meta:
        model = Profile

    name = Faker('name')


def generate(seed):
    reseed(seed)

    print('Generating profiles')
    generate_fake_data(ProfileFactory, NUM_PROFILES)
