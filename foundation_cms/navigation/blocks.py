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


class NavGroupValue(blocks.StructValue):
    @property
    def heading(self) -> str:
        return self.get("heading")

    @property
    def group_links(self):
        return self.get("links") or []

    @property
    def browse_all_link(self):
        browse_all = self.get("browse_all") or []
        return browse_all[0] if browse_all else None


class NavGroup(blocks.StructBlock):
    """
    A headed column of links in a dropdown panel.
    """

    heading = blocks.CharBlock(max_length=50, help_text="Maximum 50 characters.")
    links = blocks.ListBlock(NavLink(), min_num=1, max_num=8, label="Links")
    browse_all = blocks.ListBlock(
        NavLink(),
        min_num=0,
        max_num=1,
        default=[],
        label="Browse all link",
        help_text="Optional link shown under the group, such as a link to the whole section.",
    )

    class Meta:
        label = "Link Group"
        icon = "list-ul"
        value_class = NavGroupValue


class NavDropdownValue(blocks.StructValue):
    @property
    def header_value(self):
        return self.get("header")

    @property
    def dropdown_items(self):
        return self.get("items") or []

    @property
    def link_groups(self):
        return self.get("groups") or []

    @property
    def intro_cta_link(self):
        intro_cta = self.get("intro_cta") or []
        return intro_cta[0] if intro_cta else None

    @property
    def panel_cta_link(self):
        """The intro link, falling back to the header so the landing page stays reachable."""
        return self.intro_cta_link or self.header_value

    @property
    def has_wide_group_spacing(self) -> bool:
        return self.get("group_spacing") == "wide"

    @property
    def has_panel(self) -> bool:
        """Whether the dropdown opens a panel rather than acting as a plain link."""
        return bool(self.link_groups or self.dropdown_items)

    def iter_links(self):
        """Yield every link the dropdown renders, header first."""
        yield self.header_value
        if self.intro_cta_link:
            yield self.intro_cta_link
        if not self.link_groups:
            yield from self.dropdown_items
        for group in self.link_groups:
            yield from group.group_links
            if group.browse_all_link:
                yield group.browse_all_link


class NavDropdown(blocks.StructBlock):
    """
    One dropdown in the top nav.
    - The header labels the dropdown in the nav bar.
    - Its panel shows an optional intro and groups of links. Without groups,
      the panel falls back to the header link and up to 5 links (items).
    """

    header = NavLink(
        required=True,
        label="Dropdown Link",
        help_text=(
            "This label is shown in the nav bar. Without link groups, the dropdown panel links to this page; "
            "without groups or items, the label is a plain link to it."
        ),
    )
    items = blocks.ListBlock(
        NavLink(),
        max_num=5,
        label="Dropdown Items",
        help_text="Up to 5 links shown in the dropdown panel when it has no link groups.",
    )
    intro_eyebrow = blocks.CharBlock(
        required=False,
        max_length=50,
        label="Intro label",
        help_text="Optional small label above the intro headline. Defaults to the dropdown label.",
    )
    intro_headline = blocks.TextBlock(
        required=False,
        max_length=160,
        label="Intro headline",
        help_text="Optional statement about the section, shown beside its links. Maximum 160 characters.",
    )
    intro_cta = blocks.ListBlock(
        NavLink(),
        min_num=0,
        max_num=1,
        default=[],
        label="Intro link",
        help_text="Optional link shown under the intro headline.",
    )
    groups = blocks.ListBlock(
        NavGroup(),
        min_num=0,
        max_num=3,
        default=[],
        label="Link Groups",
        help_text="Up to 3 headed groups of links. When set, they replace the dropdown items in the panel.",
    )
    group_spacing = blocks.ChoiceBlock(
        choices=[
            ("standard", "Standard"),
            ("wide", "Wide"),
        ],
        default="standard",
        label="Group spacing",
        help_text="Space between the link groups when they stack on mobile.",
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
