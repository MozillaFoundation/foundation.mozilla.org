from random import randint, shuffle

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
    tagline = Faker('job')
    introduction = Faker('paragraph')


def get_random_profiles(max_count=5):
    """
    Return randnom profiles up to a maximum number.

    The maximum is not guranteed to be reached. Rather at least one `Profile`
    is returned, but never more than `max_count`.

    Profiles are not duplicated.

    """
    profiles = list(Profile.objects.all())
    count = len(profiles)

    shuffle(profiles)

    for i in range(0, randint(1, min(count, max_count))):
        yield profiles[i]


def generate(seed):
    reseed(seed)

    print('Generating profiles')
    generate_fake_data(ProfileFactory, NUM_PROFILES)
