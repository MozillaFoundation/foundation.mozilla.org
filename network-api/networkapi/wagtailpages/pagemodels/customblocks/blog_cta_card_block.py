from wagtail import blocks

from .base_rich_text_options import base_rich_text_options
from .image_block import ImageBlock
from .link_button_block import LinkButtonBlock

BLOG_CARD_CTA_RICH_TEXT_OPTIONS = base_rich_text_options + ["hr", "h4", "h5", "ul", "ol"]


class BlogCTACardBlock(blocks.StructBlock):
    style = blocks.ChoiceBlock(
        choices=[("pop", "Pop"), ("outline", "Outline"), ("filled", "Filled")],
        default="pop",
    )

    title = blocks.CharBlock(help_text="Optional title for the card.", max_length=100, required=False)

    body = blocks.RichTextBlock(help_text="Body text of the card.", features=BLOG_CARD_CTA_RICH_TEXT_OPTIONS)

    image = blocks.ListBlock(ImageBlock(), min_num=0, max_num=1, default=[])
    button = blocks.ListBlock(LinkButtonBlock(), min_num=0, max_num=1, default=[])

    class Meta:
        template = "wagtailpages/blocks/blog_cta_card_block.html"
        icon = "link-external"
