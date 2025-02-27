import factory
import wagtail_factories

from legacy_cms.wagtailpages.factory.customblocks.image_block import ImageBlockFactory
from legacy_cms.wagtailpages.factory.customblocks.link_button_block import (
    LinkButtonBlockFactory,
)
from legacy_cms.wagtailpages.pagemodels import customblocks


class BlogCTACardBlockFactory(wagtail_factories.StructBlockFactory):
    class Meta:
        model = customblocks.BlogCTACardBlock

    class Params:
        no_title = factory.Trait(title=None)
        no_image = factory.Trait(image=[])
        no_button = factory.Trait(button=[])

    body = factory.Faker("sentence", nb_words=10)
    title = factory.Faker("sentence", nb_words=4)
    style = factory.Faker("random_element", elements=["pop", "outline", "filled"])
    image = wagtail_factories.ListBlockFactory(ImageBlockFactory)
    button = wagtail_factories.ListBlockFactory(LinkButtonBlockFactory)
