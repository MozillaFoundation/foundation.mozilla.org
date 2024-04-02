from collections import OrderedDict

from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList
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


class NavFeaturedItem(BaseLinkBlock):
    icon = ImageChooserBlock()

    def __init__(self, local_blocks=None, **kwargs):
        # Use __init__ method to change the order of the blocks when constructing
        # them through inheritance
        super().__init__(local_blocks, **kwargs)
        self.child_blocks = self.base_blocks.copy()
        child_blocks = OrderedDict(
            {
                "label": self.child_blocks.pop("label"),
                "icon": self.child_blocks.pop("icon"),
            }
        )
        child_blocks.update({k: v for k, v in self.child_blocks.items()})
        self.child_blocks = child_blocks

    class Meta:
        value_class = NavItemValue
        label = "Featured Navigation Link"
        icon = "link"
        template = "nav/blocks/featured_item_block.html"


register(BaseLinkBlockAdapter(), NavFeaturedItem)


class NavButton(BaseLinkBlock):
    class Meta:
        value_class = NavItemValue
        label = "Navigation Button"
        icon = "link"
        template = "nav/blocks/nav_button_block.html"


register(BaseLinkBlockAdapter(), NavButton)


class NavColumnValue(blocks.StructValue):
    @property
    def has_button(self) -> bool:
        return bool(self.get("button"))

    @property
    def button(self) -> NavButton | None:
        button = self.get("button")
        if button:
            return button[0]
        return None


class NavColumn(blocks.StructBlock):
    title = blocks.CharBlock(max_length=100)
    # Empty default so that it starts collapsed:
    nav_items = blocks.ListBlock(NavItem, min_num=1, max_num=4, label="Items", default=[])
    button = blocks.ListBlock(
        NavButton,
        required=False,
        min_num=0,
        max_num=1,
        default=[],
        label="Column Button",
        help_text="Adds a CTA button to the bottom of the nav column.",
    )

    class Meta:
        label = "Navigation Column"
        icon = "list-ul"
        template = "nav/blocks/nav_column_block.html"
        value_class = NavColumnValue


class NavFeaturedColumn(blocks.StructBlock):
    title = blocks.CharBlock(max_length=100)
    # Empty default so that it starts collapsed:
    nav_items = blocks.ListBlock(NavFeaturedItem, min_num=1, max_num=4, label="Items", default=[])

    class Meta:
        label = "Featured Navigation Column"
        icon = "list-ul"
        template = "nav/blocks/featured_column_block.html"
        value_class = NavColumnValue


class NavOverview(blocks.StructBlock):
    title = blocks.CharBlock(max_length=100)
    description = blocks.RichTextBlock(features=["bold", "italic"], max_length=200)

    class Meta:
        label = "Navigation Overview"
        icon = "pilcrow"
        template = "nav/blocks/overview_block.html"


class NavDropdownValue(blocks.StructValue):
    @property
    def has_overview(self) -> bool:
        return bool(self.get("overview"))

    @property
    def overview(self) -> NavOverview | None:
        overview = self.get("overview")
        if overview:
            return overview[0]
        return None

    @property
    def has_button(self) -> bool:
        return bool(self.get("button"))

    @property
    def button(self) -> NavButton | None:
        button = self.get("button")
        if button:
            return button[0]
        return None


class NavDropdown(blocks.StructBlock):
    title = blocks.CharBlock(max_length=100, help_text="How the dropdown menu will be labelled in the nav bar")
    overview = blocks.ListBlock(
        NavOverview(label="Overview"),
        min_num=0,
        max_num=1,
        label="Overview",
        help_text="If added, the overview will take the place of the first column",
        default=[],
    )
    columns = blocks.ListBlock(
        NavColumn(label="Column"),
        min_num=1,
        max_num=4,
        label="Columns",
        help_text="Add up to 4 columns of navigation links",
    )
    button = blocks.ListBlock(
        NavButton,
        required=False,
        min_num=0,
        max_num=1,
        default=[],
        label="Dropdown Button",
        help_text="Use it to add a CTA to link to the contents of the dropdown menu",
    )

    def clean(self, value):
        result = super().clean(value)
        errors = {}

        if result["overview"] and len(result["columns"]) > 3:
            errors["overview"] = ErrorList(
                [
                    blocks.ListBlockValidationError(
                        block_errors={},
                        non_block_errors=ErrorList(
                            [ValidationError("Overview cannot be used with more than 3 nav columns.")]
                        ),
                    )
                ]
            )
            errors["columns"] = ErrorList(
                [
                    blocks.ListBlockValidationError(
                        block_errors={},
                        non_block_errors=ErrorList(
                            [ValidationError('A maximum of 3 columns can be added together with an "overview".')]
                        ),
                    )
                ]
            )

        if errors:
            raise blocks.StructBlockValidationError(block_errors=errors)

        return result

    class Meta:
        label = "Navigation Dropdown"
        icon = "bars"
        template = "nav/blocks/nav_dropdown_block.html"
        value_class = NavDropdownValue
