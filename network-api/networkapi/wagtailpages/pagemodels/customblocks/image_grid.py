from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class ImageGrid(blocks.StructBlock):
    image = ImageChooserBlock()
    alt_text = blocks.CharBlock(
        required=False,
        help_text='Alt text for this image.'
    )
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


class ImageGridBlock(blocks.StructBlock):
    grid_items = blocks.ListBlock(ImageGrid())

    class Meta:
        # this is probably the wrong icon but let's run with it for now
        icon = 'grip'
        template = 'wagtailpages/blocks/image_grid_block.html'
