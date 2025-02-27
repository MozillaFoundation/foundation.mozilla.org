import factory
import wagtail_factories

from legacy_cms.wagtailpages import models as wagtailpage_models
from legacy_cms.wagtailpages.factory import image_factory


class ResearchLibraryPageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = wagtailpage_models.ResearchLibraryPage

    title = "Library"
    banner_image = factory.SubFactory(image_factory.ImageFactory)
