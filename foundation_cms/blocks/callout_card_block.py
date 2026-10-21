from wagtail import blocks
from wagtail.images.blocks import ImageBlock

from foundation_cms.base.models.base_block import BaseBlock

from .custom_rich_text_block import CustomRichTextBlock


class CalloutCardBlock(BaseBlock):
    """POC for the Callout Card block a partial match implementation for Timely activation cards."""

    headline = blocks.CharBlock(required=False, help_text="Optional headline for the card.")
    subheading = blocks.CharBlock(required=True, help_text="Subheading for the card.")
    body = CustomRichTextBlock(required=False, help_text="Optional description text.")
    image = ImageBlock(required=True)

    class Meta:
        icon = "image"
        template_name = "callout_card_block.html"
        label = "Callout Card"
