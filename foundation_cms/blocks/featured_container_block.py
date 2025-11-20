from wagtail.blocks import ChoiceBlock, RichTextBlock, StreamBlock

from .media_block import CustomMediaBlock
from .two_column_container_block import TwoColumnContainerBlock


class ColumnStreamBlock(StreamBlock):
    rich_text = RichTextBlock()
    media = CustomMediaBlock()


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
