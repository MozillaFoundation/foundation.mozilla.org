from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

from networkapi.wagtailpages.pagemodels.customblocks.base_rich_text_options import base_rich_text_options


class NoticeBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    image_altText = blocks.CharBlock(required=True, help_text="Image description (for screen readers).")
    text = blocks.RichTextBlock(features=base_rich_text_options)

    class Meta:
        icon = "doc-full"
        template = "donate/blocks/notice_block.html"
