import factory
import wagtail_factories

from networkapi.libraries import models as library_models
from networkapi.wagtailpages.factory import image_factory


class ResearchLandingPageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = library_models.ResearchLandingPage

    title = "Research"
    banner_image = factory.SubFactory(image_factory.ImageFactory)
    intro = factory.Faker("text", max_nb_chars=250)
