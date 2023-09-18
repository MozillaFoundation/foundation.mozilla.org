import factory
import wagtail_factories

from networkapi.wagtailpages.factory.customblocks.image_block import ImageBlockFactory
from networkapi.wagtailpages.factory.customblocks.link_button_block import (
    LinkButtonBlockFactory,
)
from networkapi.wagtailpages.pagemodels import customblocks


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
