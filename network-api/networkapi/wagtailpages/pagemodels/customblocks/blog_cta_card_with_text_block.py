from wagtail import blocks

from .blog_cta_card_block import BlogCTACardBlock
from .full_content_rich_text_options import full_content_rich_text_options


class BlogCTACardWithTextBlock(blocks.StructBlock):
    alignment = blocks.ChoiceBlock(
        choices=[("right", "Right"), ("left", "Left")],
        default="right",
        help_text="For full-width cards, please use a regular Blog CTA Card block with a separate paragraph.",
    )

    paragraph = blocks.RichTextBlock(
        features=full_content_rich_text_options,
        template="wagtailpages/blocks/rich_text_block.html",
        help_text="Optional paragraph text to be displayed next to the card.",
    )

    card = BlogCTACardBlock(required=True, template="wagtailpages/blocks/blog_cta_card_block_no_wrappers.html")

    class Meta:
        template = "wagtailpages/blocks/blog_cta_card_with_text_block.html"
        icon = "form"
