from wagtail import blocks
from wagtail.telepath import register

from foundation_cms.legacy_apps.wagtailpages.pagemodels.customblocks.common.base_link_block import (
    BaseLinkBlock,
    BaseLinkBlockAdapter,
    BaseLinkValue,
)


class NavLinkValue(BaseLinkValue):
    @property
    def is_external(self) -> bool:
        return self.get("link_to") == "external_url"


class NavLink(BaseLinkBlock):
    """
    A single nav link (used both for dropdown "header link" and dropdown items).
    """

    class Meta:
        value_class = NavLinkValue
        label = "Nav Link"
        icon = "link"
        template = "fragments/blocks/nav/link.html"


register(BaseLinkBlockAdapter(), NavLink)


class NavDropdownValue(blocks.StructValue):
    @property
    def header_value(self):
        return self.get("header")

    @property
    def dropdown_items(self):
        return self.get("items") or []

class NavDropdown(blocks.StructBlock):
    """
    One dropdown in the top nav.
    - The dropdown itself is a link (header).
    - It contains up to 5 links (items).
    """

    header = NavLink(
        required=True,
        label="Dropdown Link",
        help_text="This label is shown in the nav bar and links to the dropdown landing page.",
    )
    items = blocks.ListBlock(
        NavLink(),
        required=True,
        min_num=1,
        max_num=5,
        label="Dropdown Items",
        help_text="Up to 5 links shown in the dropdown panel.",
    )

    class Meta:
        label = "Nav Dropdown"
        icon = "nav-dropdown"
        template = "fragments/blocks/nav/dropdown.html"
        value_class = NavDropdownValue


class NavValue(blocks.StructValue):
    @property
    def dropdowns(self) -> list[NavDropdownValue]:
        return self.get("dropdowns") or []


class Nav(blocks.StructBlock):
    """
    The full nav config: up to 5 dropdowns.
    """

    dropdowns = blocks.ListBlock(
        NavDropdown(),
        required=True,
        min_num=1,
        max_num=5,
        label="Dropdowns",
        help_text="Up to 5 dropdowns in the top navigation.",
    )

    class Meta:
        label = "Navigation"
        icon = "site"
        template = "fragments/blocks/nav/nav.html"
        value_class = NavValue