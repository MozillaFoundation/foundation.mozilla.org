from wagtail import blocks
from wagtail.images.blocks import ImageBlock

from foundation_cms.base.models.base_block import BaseBlock


class QuoteBlock(BaseBlock):
    is_cosmos_block = True

    quote = blocks.CharBlock(required=True, max_length=230)
    attribution = blocks.CharBlock(required=False, label="Attribution name", max_length=100)
    attribution_subtitle = blocks.CharBlock(required=False, label="Attribution subtitle", max_length=100)
    image = ImageBlock(required=False, label="Image")

    class Meta:
        icon = "doc-full"
        label = "Quote"
        template_name = "quote_block.html"
