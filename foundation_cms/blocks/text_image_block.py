from wagtail import blocks

from foundation_cms.base.models.base_block import BaseBlock

from .image_block import CustomImageBlock
from .link_block import LinkBlock


class TextImageBlock(BaseBlock):

    title = blocks.CharBlock(required=False)
    subtitle = blocks.CharBlock(required=False)
    text = blocks.RichTextBlock(required=False)
    image = CustomImageBlock(required=False)
    link = LinkBlock()

    class Meta:
        icon = "image"
        label = "Text & Image"
        template_name = "text_image_block.html"
