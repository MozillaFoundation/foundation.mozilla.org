from collections import OrderedDict

from wagtail import blocks
from wagtail.telepath import register

from networkapi.wagtailpages.pagemodels.customblocks.common.base_link_block import (
    BaseLinkBlock,
    BaseLinkBlockAdapter,
    BaseLinkValue,
)


class NavItemValue(BaseLinkValue):
    @property
    def open_in_new_window(self) -> bool:
        link_to = self.get("link_to")
        if link_to == "external_url":
            return True
        return False


class NavItem(BaseLinkBlock):
    description = blocks.CharBlock(required=False, max_length=100)

    def __init__(self, local_blocks=None, **kwargs):
        # Use __init__ method to change the order of the blocks when constructing
        # them through inheritance
        super().__init__(local_blocks, **kwargs)
        self.child_blocks = self.base_blocks.copy()
        child_blocks = OrderedDict(
            {
                "label": self.child_blocks.pop("label"),
                "description": self.child_blocks.pop("description"),
            }
        )
        child_blocks.update({k: v for k, v in self.child_blocks.items()})
        self.child_blocks = child_blocks

    class Meta:
        value_class = NavItemValue
        label = "Navigation Link"
        icon = "link"
        template = "nav/blocks/nav_link_block.html"


register(BaseLinkBlockAdapter(), NavItem)


class NavButton(BaseLinkBlock):
    class Meta:
        value_class = NavItemValue
        label = "Navigation Button"
        icon = "link"
        template = "nav/blocks/nav_button_block.html"


register(BaseLinkBlockAdapter(), NavButton)


class NavColumn(blocks.StructBlock):
    title = blocks.CharBlock(max_length=100)
    links = blocks.ListBlock(NavItem, min_num=1, max_num=4)
    button = blocks.ListBlock(NavButton, required=False, min_num=0, max_num=1)

    class Meta:
        label = "Navigation Column"
        icon = "list-ul"
        template = "nav/blocks/nav_column_block.html"
