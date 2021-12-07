from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class BannerCarouselSlideBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    heading = blocks.CharBlock(required=False)
    description = blocks.CharBlock(required=False)
