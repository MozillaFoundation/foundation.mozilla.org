from wagtail import blocks
from wagtail.telepath import register

from networkapi.wagtailpages.pagemodels.customblocks.common.base_link_block import (
    BaseLinkBlock,
    BaseLinkBlockAdapter,
    BaseLinkValue,
)


class NavLinkValue(BaseLinkValue):
    @property
    def open_in_new_window(self) -> bool:
        link_to = self.get("link_to")
        if link_to == "external_url":
            return True
        return False


class NavLinkBlock(BaseLinkBlock):
    description = blocks.CharBlock(required=False, max_length=100)

    class Meta:
        value_class = NavLinkValue
        label = "Navigation Link"
        icon = "link"
        template = "nav/blocks/nav_link_block.html"


register(BaseLinkBlockAdapter(), NavLinkBlock)
