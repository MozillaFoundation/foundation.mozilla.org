from wagtail import blocks

from foundation_cms.base.models.base_block import BaseBlock


class QuoteBlock(BaseBlock):

    quote = blocks.CharBlock(required=True)
    attribution = blocks.CharBlock(required=False)
    quote_style = blocks.ChoiceBlock(
        choices=[
            ("regular", "Regular"),
            ("large", "Large"),
            ("emphasis", "Emphasis"),
        ],
        default="regular",
        help_text="Choose the visual style for this quote.",
    )

    class Meta:
        icon = "doc-full"
        label = "Quote"
        template_name = "quote_block.html"
