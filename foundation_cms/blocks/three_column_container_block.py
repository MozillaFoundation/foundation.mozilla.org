from wagtail.blocks import ChoiceBlock

from foundation_cms.base.models.base_block import BaseBlock

from .common.background_color_block import BackgroundColorChoiceBlock
from .two_column_container_block import ColumnStreamBlock


class ThreeColumnContainerBlock(BaseBlock):
    background_color = BackgroundColorChoiceBlock()
    vertical_alignment = ChoiceBlock(
        choices=[
            ("top", "Top"),
            ("middle", "Middle"),
            ("bottom", "Bottom"),
        ],
        default="middle",
        help_text="Vertical alignment of the columns content",
    )
    left_column = ColumnStreamBlock(label="Left Column", required=False)
    center_column = ColumnStreamBlock(label="Center Column", required=False)
    right_column = ColumnStreamBlock(label="Right Column", required=False)

    class Meta:
        template_name = "three_column_container_block.html"
        icon = "placeholder"
        label = "Three Column Container"
