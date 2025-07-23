from . import BaseCardBlock
from .link_block import LinkBlock


class PortraitCardBlock(BaseCardBlock):

    cta_link = LinkBlock(required=True, label="Call to Action Link", help_text="Link for the card.")

    class Meta:
        label = "Portrait Card"
        icon = "form"
