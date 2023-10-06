from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

from networkapi.wagtailpages.pagemodels.customblocks.base_rich_text_options import base_rich_text_options


class NoticeBlock(blocks.StructBlock):
    notice_image = ImageChooserBlock()
    notice_image_altText = blocks.CharBlock(required=True, help_text="Image description (for screen readers).")
    notice_text = blocks.RichTextBlock(features=base_rich_text_options)

    class Meta:
        icon = "doc-full"
        template = "donate/blocks/notice_block.html"
