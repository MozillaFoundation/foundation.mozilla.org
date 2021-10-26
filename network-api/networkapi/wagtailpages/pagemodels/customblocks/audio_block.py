from wagtail.core import blocks
from wagtailmedia.blocks import AudioChooserBlock


class AudioBlock(blocks.StructBlock):

    audio = AudioChooserBlock()

    caption = blocks.CharBlock(
        required=False
    )

    class Meta:
        icon = 'media'
        template = 'wagtailpages/blocks/audio_block.html'
