from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from legacy_cms.utility.faker import generate_fake_data
from legacy_cms.utility.faker.helpers import reseed
from legacy_cms.wagtailpages.factory import image_factory
from legacy_cms.wagtailpages.models import Profile

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

    print("Generating a profile that can be used for percy testing.")
    ProfileFactory(
        name="Percy Profile",
        tagline="A profile made for visual regression testing.",
    )

    print("Generating other profiles")
    generate_fake_data(ProfileFactory, NUM_PROFILES)
