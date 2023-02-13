from wagtail import blocks

from ..customblocks.base_rich_text_options import base_rich_text_options
from .image_block import ImageBlock


class ImageTextMini(ImageBlock):
    text = blocks.RichTextBlock(features=base_rich_text_options)

    class Meta:
        icon = "doc-full"
        template = "wagtailpages/blocks/image_text_mini.html"
