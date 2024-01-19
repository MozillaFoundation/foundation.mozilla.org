from html import unescape

from django.forms.utils import ErrorList
from django.utils.html import strip_tags
from wagtail import blocks
from wagtail.blocks.struct_block import StructBlockValidationError

from .blog_cta_card_block import BlogCTACardBlock
from .full_content_rich_text_options import full_content_rich_text_options


class BlogCTACardWithTextBlock(blocks.StructBlock):
    alignment = blocks.ChoiceBlock(
        choices=[("right", "Right"), ("left", "Left")],
        default="right",
        help_text="For full-width cards, please use a regular Blog CTA Card block with a separate paragraph.",
    )

    card = BlogCTACardBlock(required=True, template="wagtailpages/blocks/blog_cta_card_block_regular.html")

    paragraph = blocks.RichTextBlock(
        features=full_content_rich_text_options,
        template="wagtailpages/blocks/rich_text_block.html",
        help_text="Text to be displayed next to the card.",
    )

    class Meta:
        template = "wagtailpages/blocks/blog_cta_card_with_text_block.html"
        icon = "form"

    def clean(self, value):
        result = super().clean(value)
        errors = {}

        card_body = result["card"]["body"].source
        paragraph_body = result["paragraph"].source

        paragraph_length = len(strip_tags(unescape(paragraph_body)))
        card_length = len(strip_tags(unescape(card_body))) + len(result["card"]["title"])

        if card_length > paragraph_length:
            errors["paragraph"] = ErrorList(["Paragraph content cannot be shorter than card's content."])

        if errors:
            raise StructBlockValidationError(block_errors=errors)

        return result
