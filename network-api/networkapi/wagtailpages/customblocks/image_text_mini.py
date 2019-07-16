from wagtail.core import blocks
from .image_block import ImageBlock


class ImageTextMini(ImageBlock):
    text = blocks.RichTextBlock(
        features=['bold', 'italic', 'link']
    )

    class Meta:
        icon = 'doc-full'
        template = 'wagtailpages/blocks/image_text_mini.html'
