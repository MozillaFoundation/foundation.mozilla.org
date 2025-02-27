import factory
import wagtail_factories

from legacy_cms.wagtailpages import models as wagtailpage_models
from legacy_cms.wagtailpages.factory import image_factory
from legacy_cms.wagtailpages.factory.customblocks import cta_aside_block


class ResearchLandingPageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = wagtailpage_models.ResearchLandingPage

    title = "Research"
    banner_image = factory.SubFactory(image_factory.ImageFactory)
    intro = factory.Faker("text", max_nb_chars=250)
    aside_cta = wagtail_factories.StreamFieldFactory({"cta": factory.SubFactory(cta_aside_block.CTAAsideBlockFactory)})
