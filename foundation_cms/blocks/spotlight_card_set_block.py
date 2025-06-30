from wagtail import blocks

from foundation_cms.base.models.base_block import BaseBlock

from . import OptionalLinkBlock, SpotlightCardBlock


class SpotlightCardSetBlock(BaseBlock):
    headline = blocks.CharBlock(required=False, label="Headline", help_text="Main heading for the card set.")

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
