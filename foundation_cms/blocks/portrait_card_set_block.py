from wagtail import blocks

from foundation_cms.base.models.base_block import BaseBlock

from . import OptionalLinkBlock, PortraitCardBlock


class PortraitCardSetBlock(BaseBlock):

    cards = blocks.ListBlock(
        PortraitCardBlock(),
        label="Portrait Cards",
        min_num=3,
        help_text="Minimum of 3 cards required. More than 3 will turn element into a carousel.",
    )

    class Meta:
        label = "Portrait Card Set"
        icon = "form"
        template_name = "portrait_card_set_block_grid.html"
