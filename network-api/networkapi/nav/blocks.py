from collections import OrderedDict

from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.telepath import register

from networkapi.wagtailpages.pagemodels.customblocks.common.base_link_block import (
    BaseLinkBlock,
    BaseLinkBlockAdapter,
    BaseLinkValue,
)


class NavItemValue(BaseLinkValue):
    @property
    def is_external(self) -> bool:
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
        template = "fragments/blocks/nav/item.html"


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
        template = "fragments/nav/featured_item.html"


register(BaseLinkBlockAdapter(), NavFeaturedItem)


class NavButton(BaseLinkBlock):
    class Meta:
        value_class = NavItemValue
        label = "Navigation Button"
        icon = "link"
        template = "fragments/nav/button.html"


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
        template = "fragments/nav/column.html"
        value_class = NavColumnValue


class NavFeaturedColumn(blocks.StructBlock):
    title = blocks.CharBlock(max_length=100)
    # Empty default so that it starts collapsed:
    nav_items = blocks.ListBlock(NavFeaturedItem, min_num=1, max_num=4, label="Items", default=[])

    class Meta:
        label = "Featured Navigation Column"
        icon = "list-ul"
        template = "fragments/nav/featured_column.html"
        value_class = NavColumnValue


class NavOverview(blocks.StructBlock):
    title = blocks.CharBlock(max_length=100)
    description = blocks.RichTextBlock(features=["bold", "italic"], max_length=200)

    class Meta:
        label = "Navigation Overview"
        icon = "pilcrow"
        template = "fragments/nav/overview.html"


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

    @property
    def has_featured_column(self) -> bool:
        return bool(self.get("featured_column"))

    @property
    def featured_column(self) -> NavFeaturedColumn | None:
        featured_column = self.get("featured_column")
        if featured_column:
            return featured_column[0]
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
    featured_column = blocks.ListBlock(
        NavFeaturedColumn(label="Featured Column"),
        min_num=0,
        max_num=1,
        label="Featured Column",
        help_text="A column made of items and icons. If added, it will take the place of the last column",
        default=[],
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

        has_overview = bool(result["overview"])
        has_featured_column = bool(result["featured_column"])

        allowed_number_of_columns = 4
        if has_overview:
            allowed_number_of_columns -= 1
        if has_featured_column:
            allowed_number_of_columns -= 1

        current_number_of_columns = len(result["columns"])

        if current_number_of_columns > allowed_number_of_columns:
            if has_overview and not has_featured_column:
                err_msg_overview = 'A maximum of 3 columns can be added together with an "overview".'
                err_msg_columns = 'A maximum of 3 columns can be added together with an "overview".'
                err_msg_featured_column = ""
            elif has_featured_column and not has_overview:
                err_msg_overview = ""
                err_msg_columns = 'A maximum of 3 columns can be added together with a "featured column".'
                err_msg_featured_column = "Featured column cannot be used with more than 3 nav columns."
            elif has_overview and has_featured_column:
                err_msg_overview = (
                    'A maximum of 2 columns can be added together with an "overview" and a "featured column".'
                )
                err_msg_columns = (
                    'A maximum of 2 columns can be added together with an "overview" and a "featured column".'
                )
                err_msg_featured_column = (
                    'A maximum of 2 columns can be added together with an "overview" and a "featured column".'
                )

            if err_msg_overview:
                errors["overview"] = ErrorList(
                    [
                        blocks.ListBlockValidationError(
                            block_errors={},
                            non_block_errors=ErrorList([ValidationError(err_msg_overview)]),
                        )
                    ]
                )

            if err_msg_featured_column:
                errors["featured_column"] = ErrorList(
                    [
                        blocks.ListBlockValidationError(
                            block_errors={},
                            non_block_errors=ErrorList([ValidationError(err_msg_featured_column)]),
                        )
                    ]
                )

            errors["columns"] = ErrorList(
                [
                    blocks.ListBlockValidationError(
                        block_errors={},
                        non_block_errors=ErrorList([ValidationError(err_msg_columns)]),
                    )
                ]
            )

        if errors:
            raise blocks.StructBlockValidationError(block_errors=errors)

        return result

    class Meta:
        label = "Navigation Dropdown"
        icon = "bars"
        template = "fragments/nav/dropdown.html"
        value_class = NavDropdownValue
