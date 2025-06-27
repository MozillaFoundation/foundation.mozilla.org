from foundation_cms.base.models.base_block import BaseBlock
from foundation_cms.blocks.link_block import LinkBlock
from wagtail import blocks


class LinkButtonBlock(BaseBlock, LinkBlock):

    style = blocks.ChoiceBlock(
        choices=[
            ("btn-primary", "Primary"),
            ("btn-secondary", "Secondary"),
        ],
        default="btn-primary",
    )

    class Meta:
        icon = "link"
        template_name = "link_button_block.html"
