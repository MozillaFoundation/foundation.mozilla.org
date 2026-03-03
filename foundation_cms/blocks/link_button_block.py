from wagtail import blocks

from foundation_cms.base.models.base_block import BaseBlock
from foundation_cms.blocks.link_block import LinkBlock


class LinkButtonBlock(BaseBlock, LinkBlock):

    style = blocks.ChoiceBlock(
        choices=[
            ("btn-primary", "Primary"),
            ("btn-secondary", "Secondary"),
        ],
        default="btn-primary",
    )
    alignment = blocks.ChoiceBlock(
        choices=[
            ("link-button-block__left", "Left"),
            ("link-button-block__center", "Center"),
        ],
        default="btn-left",
    )

    class Meta:
        icon = "link"
        template_name = "link_button_block.html"
