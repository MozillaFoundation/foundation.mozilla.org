import factory
import wagtail_factories

from foundation_cms.profiles.models import Profile, ProfilePage


class ProfileFactory(factory.django.DjangoModelFactory):
    """
    Factory for the Profile model
    """
    class Meta:
        model = Profile

    title = factory.Faker("name")


class ProfilePageFactory(wagtail_factories.PageFactory):
    """
    Factory for the Profile model
    """
    class Meta:
        model = ProfilePage

    bio = factory.Faker("paragraph")
    profile = factory.SubFactory(ProfileFactory)
