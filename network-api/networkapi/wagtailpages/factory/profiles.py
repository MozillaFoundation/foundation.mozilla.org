from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from networkapi.utility.faker import generate_fake_data
from networkapi.utility.faker.helpers import reseed
from networkapi.wagtailpages.factory import image_factory
from networkapi.wagtailpages.models import Profile

NUM_PROFILES = 10


class ProfileFactory(DjangoModelFactory):
    class Meta:
        model = Profile

    name = Faker("name")
    tagline = Faker("text", max_nb_chars=50)
    introduction = Faker("paragraph")
    image = SubFactory(image_factory.ImageFactory)


def generate(seed):
    reseed(seed)

    print("Generating profile for percy testing use")
    ProfileFactory(
        name="Percy Profile",
        tagline="This is a author profile specifically created for visual regression testing",
    )

    print("Generating other profiles")
    generate_fake_data(ProfileFactory, NUM_PROFILES)
