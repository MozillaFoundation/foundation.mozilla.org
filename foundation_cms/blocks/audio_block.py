from wagtail import blocks
from wagtail.images.blocks import ImageBlock

from foundation_cms.base.models.base_block import BaseBlock


class AudioBlock(BaseBlock):
    image = ImageBlock(required=False, help_text="Optional image to display at the top of the block.")
    title = blocks.CharBlock()
    description = blocks.TextBlock(required=False, help_text="Short description of the audio")
    simplecast_embed_code = blocks.CharBlock()

    class Meta:
        icon = "media"
        template_name = "audio_block.html"
