from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class ImageBlock(blocks.StructBlock):
    image = ImageChooserBlock()

    altText = blocks.CharBlock(required=True, help_text="Image description (for screen readers).")

    class Meta:
        icon = "image"
        template = "wagtailpages/blocks/image_block.html"
