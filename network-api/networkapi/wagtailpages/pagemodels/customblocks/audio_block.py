from wagtail.core import blocks
from wagtailmedia.blocks import AbstractMediaChooserBlock
from django.forms.utils import flatatt
from django.utils.html import format_html, format_html_join


class AudioBlock(blocks.StructBlock):

    audio = AbstractMediaChooserBlock()

    caption = blocks.CharBlock(
        required=False
    )

    class Meta:
        icon = 'media'
        template = 'wagtailpages/blocks/audio_block.html'
