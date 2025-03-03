import factory

from foundation_cms.legacy_cms.wagtailpages.factory.customblocks.link_block import LinkBlockFactory
from foundation_cms.legacy_cms.wagtailpages.pagemodels import customblocks


class LinkButtonBlockFactory(LinkBlockFactory):
    class Meta:
        model = customblocks.LinkButtonBlock

    styling = factory.Faker("random_element", elements=["btn-primary", "btn-secondary"])
