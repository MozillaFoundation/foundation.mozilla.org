from . import BaseCardBlock
from .link_block import OptionalLinkWithoutLabelBlock


class PortraitCardBlock(BaseCardBlock):

    cta_link = OptionalLinkWithoutLabelBlock(required=False, label="Call to Action Link", help_text="Optional link for the card.")
    class Meta:
        label = "Portrait Card"
        icon = "form"
