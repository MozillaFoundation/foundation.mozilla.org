from wagtail.blocks import StructBlock, StreamBlock, RichTextBlock, CharBlock
from .audio_block import AudioBlock # Just as an example second block

class ColumnStreamBlock(StreamBlock):
    rich_text = RichTextBlock()
    audio = AudioBlock()

class TwoColumnContainerBlock(StructBlock):
    title = CharBlock(required=False, help_text="Optional title for the block")
    left_column = ColumnStreamBlock(label="Left Column")
    right_column = ColumnStreamBlock(label="Right Column")

    class Meta:
        template = "patterns/blocks/themes/default/two_column_container_block.html"
        icon = "placeholder"
        label = "Two Column Container"