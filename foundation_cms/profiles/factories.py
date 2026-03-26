import factory
import wagtail_factories

from foundation_cms.profiles.models import ExpertProfilePage


class ExpertProfilePageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = ExpertProfilePage

    role = factory.Faker("job")
    bio = factory.Faker("paragraph")
    location = factory.Faker("country")
    image = factory.SubFactory(wagtail_factories.ImageFactory)
