from wagtail import blocks
from wagtailmedia.blocks import AudioChooserBlock
from foundation_cms.base.models.base_block import BaseBlock
from wagtail.images.blocks import ImageChooserBlock


class AudioBlock(BaseBlock):
    audio = AudioChooserBlock()
    title = blocks.CharBlock()
    description = blocks.TextBlock(required=False, help_text="Short description of the audio")
    image = ImageChooserBlock(required=False)
    image_alt_text = blocks.CharBlock(required=False, help_text="Image description (for screen readers).")

    class Meta:
        icon = "media"
        template_name = "audio_block.html"
