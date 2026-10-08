from wagtail import blocks

from foundation_cms.base.models.base_block import BaseBlock
from foundation_cms.blocks.link_block import LinkBlock


class CallToActionBlock(BaseBlock):
    heading = blocks.CharBlock(max_length=100)
    body = blocks.TextBlock(required=False, max_length=250)
    button = LinkBlock()

    class Meta:
        icon = "pick"
        label = "Call to Action"
        template_name = "call_to_action_block.html"
