import factory
import wagtail_factories

from foundation_cms.legacy_apps.wagtailpages.factory.customblocks.blog_cta_card_block import (
    BlogCTACardBlockFactory,
)
from foundation_cms.legacy_apps.wagtailpages.pagemodels import customblocks


class BlogCTACardWithTextBlockFactory(wagtail_factories.StructBlockFactory):
    class Meta:
        model = customblocks.BlogCTACardWithTextBlock

    card = factory.SubFactory(BlogCTACardBlockFactory)
    alignment = factory.Faker("random_element", elements=["right", "left"])
    paragraph = factory.Faker("paragraph")
