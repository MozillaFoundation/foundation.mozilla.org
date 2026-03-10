from wagtail.blocks import (
    CharBlock,
    ChoiceBlock,
    ListBlock,
    RichTextBlock,
    StructBlock,
)

from foundation_cms.base.models.base_block import BaseBlock


# Predefined icon library with alt text by default - only approved icons can be used
ICON_CHOICES = [
    ("chat", "Chat icon"),
    ("eye-open", "Eye Open icon"),
    ("gear", "Gear icon"),
    ("globe", "Globe icon"),
    ("megaphone", "Megaphone icon"),
    ("star", "Star icon"),
    # Add more icons as needed
]


class IconInfoGridItemBlock(StructBlock):
    """Individual grid item with icon, title, and optional description"""

    icon = ChoiceBlock(
        choices=ICON_CHOICES,
        required=True,
        help_text="Select an icon for this item",
    )
    title = CharBlock(
        required=True,
        max_length=100,
        help_text="Title for this item",
    )
    description = CharBlock(
        required=False,
        max_length=126,
        help_text="Optional description (max 126 characters)",
    )

    class Meta:
        icon = "info-circle"
        label = "Icon Info Item"


class IconInfoGridBlock(BaseBlock):
    """
    Grid block for displaying informational content with icons.
    """

    heading = CharBlock(
        required=True,
        max_length=100,
        help_text="Section heading for this grid",
    )
    
    icon_color = ChoiceBlock(
        choices=[
            ("orange", "Orange"),
            ("black", "Black"),
        ],
        default="orange",
        help_text="Color applied to all icons in this grid",
    )

    columns = ChoiceBlock(
        choices=[
            ("1", "1 column"),
            ("2", "2 columns"),
            ("3", "3 columns"),
        ],
        default="3",
        help_text="Number of columns on desktop (automatically stacks on mobile)",
        label="Number of columns for this grid",
    )

    layout_style = ChoiceBlock(
        choices=[
            ("compact", "Compact (icons + titles only)"),
            ("detailed", "Detailed (icons + titles + descriptions)"),
        ],
        default="compact",
        help_text="Choose content density. Compact hides descriptions, Detailed shows them.",
        label="Layout style",
    )
    
    items = ListBlock(
        IconInfoGridItemBlock(),
        min_num=1,
        max_num=12,
        help_text="Add up to 12 icon info items",
    )

    class Meta:
        icon = "grip"
        label = "Icon Info Grid"
        template_name = "icon_info_grid_block.html"
