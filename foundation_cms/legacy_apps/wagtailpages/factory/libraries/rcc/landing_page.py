import factory
import wagtail_factories

from foundation_cms.legacy_apps.wagtailpages import models as wagtailpage_models
from foundation_cms.legacy_apps.wagtailpages.factory import image_factory
from foundation_cms.legacy_apps.wagtailpages.factory.customblocks import cta_aside_block


class RCCLandingPageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = wagtailpage_models.RCCLandingPage

    title = "Responsible Computing Challenge Playbook"
    banner_image = factory.SubFactory(image_factory.ImageFactory)
    intro = factory.Faker("text", max_nb_chars=250)
    aside_cta = wagtail_factories.StreamFieldFactory({"cta": factory.SubFactory(cta_aside_block.CTAAsideBlockFactory)})
