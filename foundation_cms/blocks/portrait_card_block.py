from . import BaseCardBlock
from .link_block import LinkWithoutLabelBlock


class PortraitCardBlock(BaseCardBlock):

    cta_link = LinkWithoutLabelBlock(
        required=True, label="Call to Action Link", help_text="Link for the card."
    )

    class Meta:
        label = "Portrait Card"
        icon = "form"
