from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class ImageGridAltText(blocks.StructValue):
    """Get alt_text or default to image title."""

    def alt(self):
        alt_text = self.get('alt_text')
        image = self.get('image')
        if alt_text:
            return alt_text
        return image.title


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

    class Meta:
        value_class = ImageGridAltText


class ImageGridBlock(blocks.StructBlock):
    grid_items = blocks.ListBlock(ImageGrid())

    class Meta:
        # this is probably the wrong icon but let's run with it for now
        icon = 'grip'
        template = 'wagtailpages/blocks/image_grid_block.html'
