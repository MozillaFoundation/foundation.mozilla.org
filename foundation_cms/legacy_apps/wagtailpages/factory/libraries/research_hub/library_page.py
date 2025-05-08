import factory
import wagtail_factories

from foundation_cms.legacy_apps.wagtailpages import models as wagtailpage_models
from foundation_cms.legacy_apps.wagtailpages.factory import image_factory


class ResearchLibraryPageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = wagtailpage_models.ResearchLibraryPage

    title = "Library"
    banner_image = factory.SubFactory(image_factory.ImageFactory)
