import factory
import wagtail_factories

from foundation_cms.profiles.models import ExpertProfilePage


class ExpertProfilePageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = ExpertProfilePage

    role = factory.Faker("job")
    bio = factory.Faker("paragraph")
    location = factory.Iterator(["US", "DE", "BR", "KE", "JP"])
    image = factory.SubFactory(wagtail_factories.ImageFactory)
    seo_title = factory.Faker("sentence")
    search_description = factory.Faker("paragraph")
