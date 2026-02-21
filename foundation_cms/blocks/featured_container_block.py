from wagtail.blocks import ChoiceBlock, StreamBlock

from .custom_rich_text_block import CustomRichTextBlock
from .media_block import CustomMediaBlock
from .spacer_block import SpacerBlock
from .two_column_container_block import TwoColumnContainerBlock


class ColumnStreamBlock(StreamBlock):
    rich_text = CustomRichTextBlock()
    media = CustomMediaBlock()
    spacer = SpacerBlock()


class FeaturedContainerBlock(TwoColumnContainerBlock):
    sticky = ChoiceBlock(
        choices=[
            ("none", "None"),
            ("left", "Left Column"),
            ("right", "Right Column"),
        ],
        default="none",
        help_text="Make one column sticky on scroll",
    )

    left_column = ColumnStreamBlock(label="Left Column", required=False)
    right_column = ColumnStreamBlock(label="Right Column", required=False)

    class Meta:
        template_name = "featured_container_block.html"
        icon = "placeholder"
        label = "Featured Container"
