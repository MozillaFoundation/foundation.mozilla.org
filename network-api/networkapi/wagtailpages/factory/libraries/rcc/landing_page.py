import factory
import wagtail_factories

from networkapi.wagtailpages import models as wagtailpage_models
from networkapi.wagtailpages.factory import image_factory


class RCCLandingPageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = wagtailpage_models.RCCLandingPage

    title = "Responsible Computing Challenge Playbook"
    banner_image = factory.SubFactory(image_factory.ImageFactory)
    intro = factory.Faker("text", max_nb_chars=250)
