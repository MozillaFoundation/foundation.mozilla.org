from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from foundation_cms.legacy_apps.utility.faker import generate_fake_data
from foundation_cms.legacy_apps.utility.faker.helpers import reseed
from foundation_cms.legacy_apps.wagtailpages.factory.image_factory import ImageFactory
from foundation_cms.legacy_apps.wagtailpages.models import Profile

NUM_PROFILES = 10


class ProfileFactory(DjangoModelFactory):
    class Meta:
        model = Profile

    name = Faker("name")
    tagline = Faker("text", max_nb_chars=50)
    introduction = Faker("paragraph")
    image = SubFactory(ImageFactory)


def generate(seed):
    reseed(seed)

    print("Generating a profile that can be used for percy testing.")
    ProfileFactory(
        name="Percy Profile",
        tagline="A profile made for visual regression testing.",
    )

    print("Generating other profiles")
    generate_fake_data(ProfileFactory, NUM_PROFILES)
