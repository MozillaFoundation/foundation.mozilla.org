from wagtail import blocks

from foundation_cms.base.models.base_block import BaseBlock

from . import OptionalLinkBlock, PillarCardBlock


class PillarCardSetBlock(BaseBlock):
    cards = blocks.ListBlock(
        PillarCardBlock(),
        label="Pillar Cards",
        min_num=3,
        max_num=3,
        help_text="3 cards required.",
    )

    class Meta:
        label = "Pillar Card Set"
        icon = "form"
        template_name = "pillar_card_set_block.html"
