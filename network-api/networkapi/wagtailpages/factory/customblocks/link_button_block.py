import factory

from networkapi.wagtailpages.factory.customblocks.link_block import LinkBlockFactory
from networkapi.wagtailpages.pagemodels import customblocks


class LinkButtonBlockFactory(LinkBlockFactory):
    class Meta:
        model = customblocks.LinkButtonBlock

    styling = factory.Faker("random_element", elements=["btn-primary", "btn-secondary"])
