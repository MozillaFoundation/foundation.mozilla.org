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


class ImageTextMini(ImageBlock):
    text = blocks.RichTextBlock(
        features=['bold', 'italic', 'link']
    )

    class Meta:
        icon = 'doc-full'
        template = 'wagtailpages/blocks/image_text_mini.html'
