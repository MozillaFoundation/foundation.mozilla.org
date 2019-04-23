from wagtail.core import blocks

from .image_grid import ImageGrid


class ImageGridBlock(blocks.StructBlock):
    grid_items = blocks.ListBlock(ImageGrid())

    class Meta:
        # this is probably the wrong icon but let's run with it for now
        icon = 'grip'
        template = 'wagtailpages/blocks/image_grid_block.html'
