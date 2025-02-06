import factory
from foundation_cms.profiles.models import Profile


class ProfileFactory(factory.django.DjangoModelFactory):
    """
    Factory for the Profile model
    """
    class Meta:
        model = Profile

    title = factory.Faker("name")