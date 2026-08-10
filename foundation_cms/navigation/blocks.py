from urllib.parse import urlencode

from django.urls import reverse
from wagtail import blocks
from wagtail.admin.telepath import register

from foundation_cms.legacy_apps.wagtailpages.pagemodels.customblocks.common.base_link_block import (
    BaseLinkBlock,
    BaseLinkBlockAdapter,
    BaseLinkValue,
)


class NavLinkValue(BaseLinkValue):
    target_fields = ("page", "external_url", "relative_url")

    @property
    def resolved_link_to(self):
        """Return the selected link type, including translated values missing link_to."""
        if link_to := self.get("link_to"):
            return link_to

        return next((field for field in self.target_fields if self.get(field)), None)

    @property
    def is_external(self) -> bool:
        return self.resolved_link_to == "external_url"

    def get_url_for_request(self, request):
        """Resolve PageChooser URLs relative to the site serving the request."""
        if self.resolved_link_to != "page":
            return self.url

        page = self.get("page")
        return page.localized.get_url(request=request) if page else None

    @property
    def label(self) -> str:
        return self.get("label")


class NavLink(BaseLinkBlock):
    """
    A single nav link (used both for dropdown "header link" and dropdown items).
    """

    label = blocks.CharBlock(max_length=36, help_text="Maximum 36 characters.")

    class Meta:
        value_class = NavLinkValue
        label = "Nav Link"
        icon = "link"
        template = "fragments/blocks/nav/link.html"


register(BaseLinkBlockAdapter(), NavLink)


class SearchTopicLinkValue(blocks.StructValue):
    @property
    def label(self) -> str:
        return self.get("label")

    @property
    def query(self) -> str:
        return self.get("query")

    @property
    def url(self) -> str:
        return f"{reverse('search')}?{urlencode({'query': self.query})}"


class SearchTopicLink(blocks.StructBlock):
    """
    A topic pill that links to the site search page with a configured query.
    """

    label = blocks.CharBlock(max_length=36, help_text="Maximum 36 characters.")
    query = blocks.CharBlock(max_length=100, help_text="Search query used when this topic pill is selected.")

    class Meta:
        label = "Search Topic Link"
        icon = "search"
        value_class = SearchTopicLinkValue


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
