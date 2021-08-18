from wagtail.core import blocks
from wagtailmedia.blocks import AbstractMediaChooserBlock


class AudioBlock(blocks.StructBlock):

    audio = AbstractMediaChooserBlock()

    caption = blocks.CharBlock(
        required=False
    )

    class Meta:
        icon = 'media'
        template = 'wagtailpages/blocks/audio_block.html'
