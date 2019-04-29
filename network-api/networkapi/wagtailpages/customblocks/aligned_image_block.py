from wagtail.core import blocks

from .image_block import ImageBlock


class AlignedImageBlock(ImageBlock):
    alignment = blocks.ChoiceBlock(
        choices=[
            ('', 'Do not apply any explicit alignment classes.'),
            ('left-align', 'Left-align this image with the page content.'),
            ('right-align', 'Right-align this image with the page content.'),
            ('center', 'Center this image with the page content.'),
            ('full-width', 'Make this image full-width.'),
        ],
        default='',
        required=False
    )

    class Meta:
        icon = 'image'
        template = 'wagtailpages/blocks/aligned_image_block.html'
