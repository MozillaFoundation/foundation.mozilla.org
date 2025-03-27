import factory
import wagtail_factories

from networkapi.wagtailpages import models as wagtailpage_models
from networkapi.wagtailpages.factory.customblocks import cta_aside_block
from networkapi.wagtailpages.factory.image_factory import ImageFactory


class RCCLandingPageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = wagtailpage_models.RCCLandingPage

    title = "Responsible Computing Challenge Playbook"
    banner_image = factory.SubFactory(ImageFactory)
    intro = factory.Faker("text", max_nb_chars=250)
    aside_cta = wagtail_factories.StreamFieldFactory({"cta": factory.SubFactory(cta_aside_block.CTAAsideBlockFactory)})
