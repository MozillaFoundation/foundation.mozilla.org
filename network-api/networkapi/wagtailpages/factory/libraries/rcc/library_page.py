import factory
import wagtail_factories

from networkapi.wagtailpages import models as wagtailpage_models
from networkapi.wagtailpages.factory import image_factory


class RCCLibraryPageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = wagtailpage_models.RCCLibraryPage

    title = "Curriculum Library"
    banner_image = factory.SubFactory(image_factory.ImageFactory)
