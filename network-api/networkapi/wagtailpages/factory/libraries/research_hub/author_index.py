import factory
import wagtail_factories

from networkapi.wagtailpages import models as wagtailpage_models
from networkapi.wagtailpages.factory.image_factory import ImageFactory



class ResearchAuthorsIndexPageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = wagtailpage_models.ResearchAuthorsIndexPage

    title = "Authors"
    banner_image = factory.SubFactory(ImageFactory)
