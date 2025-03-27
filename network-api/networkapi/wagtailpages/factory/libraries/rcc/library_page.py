import factory
import wagtail_factories

from networkapi.wagtailpages import models as wagtailpage_models
from networkapi.wagtailpages.factory.image_factory import ImageFactory


class RCCLibraryPageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = wagtailpage_models.RCCLibraryPage

    title = "Curriculum Library"
    banner_image = factory.SubFactory(ImageFactory)
