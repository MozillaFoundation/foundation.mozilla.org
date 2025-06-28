from typing import Any, Dict, List

from wagtail import blocks

from foundation_cms.base.models.base_block import BaseBlock
from foundation_cms.blocks.pillar_card_block import PillarCardBlock

NUM_PILLAR_CARDS = 3
DEFAULT_PILLAR_CARDS: List[Dict[str, Any]] = [
    {"headline": "", "image": None, "cta_link": []} for _ in range(NUM_PILLAR_CARDS)
]


class PillarCardSetBlock(BaseBlock):
    cards = blocks.ListBlock(
        PillarCardBlock(),
        label="Pillar Cards",
        min_num=NUM_PILLAR_CARDS,
        max_num=NUM_PILLAR_CARDS,
        help_text="3 cards required.",
        default=DEFAULT_PILLAR_CARDS,
    )

    class Meta:
        label = "Pillar Card Set"
        icon = "form"
        template_name = "pillar_card_set_block.html"
