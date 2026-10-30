from wagtail import blocks
from wagtail.admin.telepath import register

from foundation_cms.base.models.base_block import BaseBlock
from foundation_cms.blocks.common.link_block.base_link_block import (
    BaseLinkBlock,
    BaseLinkBlockAdapter,
)


class SuperCTABlock(BaseBlock, BaseLinkBlock):
    is_cosmos_block = True

    label = blocks.CharBlock(
        max_length=30,
        help_text=(
            'Say where the link goes, for example "Explore all our work". '
            'Avoid vague labels like "Click here" or "Learn more": screen reader users '
            "often hear links out of context."
        ),
    )

    class Meta:
        icon = "arrow-right"
        label = "Super CTA"
        template_name = "super_cta_block.html"


register(BaseLinkBlockAdapter(), SuperCTABlock)
