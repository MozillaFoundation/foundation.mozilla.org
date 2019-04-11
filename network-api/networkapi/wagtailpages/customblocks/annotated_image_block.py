from wagtail.images.blocks import ImageChooserBlock
from wagtail.core import blocks


class ImageBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    altText = blocks.CharBlock(
        required=True,
        help_text='Image description (for screen readers).'
    )

    class Meta:
        icon = 'image'
        template = 'wagtailpages/blocks/image_block.html'


class AnnotatedImageBlock(ImageBlock):
    caption = blocks.CharBlock(
        required=False
    )
    captionURL = blocks.CharBlock(
        required=False,
        help_text='Optional URL that this caption should link out to.'
    )

    class Meta:
        icon = 'image'
        template = 'wagtailpages/blocks/annotated_image_block.html'
        help_text = 'Design Guideline: Please crop images to a 16:6 aspect ratio when possible.'
