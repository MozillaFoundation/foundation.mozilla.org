from wagtail import blocks

from foundation_cms.base.models.base_block import BaseBlock

from . import SpotlightCardBlock
from .decorators import full_bleed_on


@full_bleed_on("*")
class SpotlightCardSetBlock(BaseBlock):

    cards = blocks.ListBlock(
        SpotlightCardBlock(),
        label="Spotlight Cards",
        min_num=3,
        max_num=3,
        help_text="3 cards required.",
    )

    class Meta:
        label = "Spotlight Card Set"
        icon = "form"
        template_name = "spotlight_card_set_block.html"
