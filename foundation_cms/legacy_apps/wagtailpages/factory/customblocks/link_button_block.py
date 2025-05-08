import factory

from foundation_cms.legacy_apps.wagtailpages.factory.customblocks.link_block import (
    LinkBlockFactory,
)
from foundation_cms.legacy_apps.wagtailpages.pagemodels import customblocks


class LinkButtonBlockFactory(LinkBlockFactory):
    class Meta:
        model = customblocks.LinkButtonBlock

    styling = factory.Faker("random_element", elements=["btn-primary", "btn-secondary"])
