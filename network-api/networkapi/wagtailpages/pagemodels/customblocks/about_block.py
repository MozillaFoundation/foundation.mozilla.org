from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

from .base_rich_text_options import base_rich_text_options


class AboutBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    image_alt_text = blocks.CharBlock(required=True, help_text="Image description (for screen readers).")
    heading = blocks.CharBlock(help_text="Heading for the About Block")
    content = blocks.RichTextBlock(features=base_rich_text_options)

    class Meta:
        template = "wagtailpages/blocks/about_block.html"
