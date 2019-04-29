from wagtail.core import blocks

from wagtail.images.blocks import ImageChooserBlock


class FigureBlock2(blocks.StructBlock):
    image = ImageChooserBlock()
    caption = blocks.CharBlock(
        required=False,
        help_text='Please remember to properly attribute any images we use.'
    )
    url = blocks.CharBlock(
        required=False,
        help_text='Optional URL that this figure should link out to.',
    )
    square_image = blocks.BooleanBlock(
        default=True,
        required=False,
        help_text='If left checked, the image will be cropped to be square.'
    )
