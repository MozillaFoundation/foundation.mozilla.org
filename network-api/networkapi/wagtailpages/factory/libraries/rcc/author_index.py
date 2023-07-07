import factory
import wagtail_factories

from networkapi.wagtailpages import models as wagtailpage_models
from networkapi.wagtailpages.factory import image_factory


class RCCAuthorsIndexPageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = wagtailpage_models.RCCAuthorsIndexPage

    title = "Browse Authors"
    banner_image = factory.SubFactory(image_factory.ImageFactory)
