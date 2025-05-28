from wagtail.blocks import CharBlock, RichTextBlock, StreamBlock, StructBlock

from foundation_cms.base.models.base_block import BaseBlock

from .audio_block import AudioBlock  # Just as an example second block
from .image_block import CustomImageBlock


class ColumnStreamBlock(StreamBlock):
    rich_text = RichTextBlock()
    audio = AudioBlock()
    image = CustomImageBlock()


class TwoColumnContainerBlock(BaseBlock):
    title = CharBlock(required=False, help_text="Optional title for the block")
    left_column = ColumnStreamBlock(label="Left Column")
    right_column = ColumnStreamBlock(label="Right Column")

    class Meta:
        template_name = "two_column_container_block.html"
        icon = "placeholder"
        label = "Two Column Container"
