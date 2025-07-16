from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

from foundation_cms.base.models.base_block import BaseBlock


class AudioBlock(BaseBlock):
    image = ImageChooserBlock(required=False, help_text="Optional image to display at the top of the block.")
    image_alt_text = blocks.CharBlock(required=False, help_text="Image description (for screen readers).")
    title = blocks.CharBlock()
    description = blocks.TextBlock(required=False, help_text="Short description of the audio")
    simplecast_embed_code = blocks.CharBlock()

    class Meta:
        icon = "media"
        template_name = "audio_block.html"
