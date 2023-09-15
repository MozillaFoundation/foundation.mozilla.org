from django.core.exceptions import ValidationError
from wagtail import blocks

from .blog_cta_card_block import BlogCTACardBlock
from .full_content_rich_text_options import full_content_rich_text_options


class BlogCTACardWithTextBlock(blocks.StructBlock):
    card = BlogCTACardBlock(required=True, template="wagtailpages/blocks/blog_cta_card_block_no_wrappers.html")

    alignment = blocks.ChoiceBlock(
        choices=[("right", "Right"), ("left", "Left"), ("full-width", "Full width")],
        default="right",
    )

    paragraph = blocks.RichTextBlock(
        features=full_content_rich_text_options,
        template="wagtailpages/blocks/rich_text_block.html",
        help_text="Optional paragraph text to be displayed next to the card.",
    )

    class Meta:
        template = "wagtailpages/blocks/blog_cta_card_with_text_block.html"

    def clean(self, value):
        result = super().clean(value)
        if result["alignment"] == "full-width" and result["paragraph"]:
            raise ValidationError(
                "Paragraph text should not be used for full width cards."
                "Please use a regular Blog CTA Card block with a separate paragraph instead."
            )
        return result
