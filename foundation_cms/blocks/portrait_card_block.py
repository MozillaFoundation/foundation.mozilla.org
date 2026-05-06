from wagtail.blocks import CharBlock

from . import BaseCardBlock
from .link_block import LinkWithDynamicLabelBlock


class PortraitCardBlock(BaseCardBlock):

    headline = CharBlock(
        required=False, max_length=36, label="Headline", help_text="Appears as the main heading (max 36 characters)."
    )
    cta_link = LinkWithDynamicLabelBlock(
        label_max_length=36, required=True, label="Call to Action Link", help_text="Link for the card."
    )

    class Meta:
        label = "Portrait Card"
        icon = "form"
