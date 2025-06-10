from wagtail import blocks

from foundation_cms.base.models.base_block import BaseBlock


class QuoteBlock(BaseBlock):

    quote = blocks.CharBlock(required=True)
    attribution = blocks.CharBlock(required=False)

    class Meta:
        icon = "doc-full"
        label = "Quote"
        template_name = "quote_block.html"
