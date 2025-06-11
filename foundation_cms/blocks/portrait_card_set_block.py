from wagtail import blocks

from foundation_cms.base.models.base_block import BaseBlock

from . import OptionalLinkBlock, PortraitCardBlock


class PortraitCardSetBlock(BaseBlock):
    headline = blocks.CharBlock(required=False, label="Headline", help_text="Main heading for the card set.")

    cards = blocks.ListBlock(
        PortraitCardBlock(),
        label="Portrait Cards",
        min_num=3,
        help_text="Minimum of 3 cards required. More than 3 will turn element into a carousel.",
    )

    cta_link = OptionalLinkBlock(
        required=False, label="Call to Action Link", help_text="Optional link below the cards."
    )

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        card_count = len(value.get("cards", []))
        theme = self.get_theme(parent_context or {})
        layout = "portrait_card_set_block_carousel.html" if card_count > 3 else "portrait_card_set_block_grid.html"
        context["card_set_template"] = f"patterns/blocks/themes/{theme}/{layout}"
        return context
    
    class Meta:
        label = "Portrait Card Set"
        icon = "form"
        template_name = "portrait_card_set_block.html"
