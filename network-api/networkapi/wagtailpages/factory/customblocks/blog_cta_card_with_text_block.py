import factory
import wagtail_factories

from networkapi.wagtailpages.factory.customblocks.blog_cta_card_block import (
    BlogCTACardBlockFactory,
)
from networkapi.wagtailpages.pagemodels import customblocks


class BlogCTACardWithTextBlockFactory(wagtail_factories.StructBlockFactory):
    class Meta:
        model = customblocks.BlogCTACardWithTextBlock

    card = factory.SubFactory(BlogCTACardBlockFactory)
    alignment = factory.Faker("random_element", elements=["right", "left"])
    paragraph = factory.Faker("paragraph")
