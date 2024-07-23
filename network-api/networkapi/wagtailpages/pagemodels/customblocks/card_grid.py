from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from networkapi.wagtailpages.pagemodels.customblocks.link_block import LinkBlock

class CardGrid(blocks.StructBlock):
    image = ImageChooserBlock()

    alt_text = blocks.CharBlock(required=False, help_text="Alt text for card's image.")

    title = blocks.CharBlock(help_text="Heading for the card.")

    body = blocks.TextBlock(help_text="Body text of the card.")

    link = blocks.ListBlock(
        LinkBlock(), min_num=0, max_num=1, help_text="Optional link that this card should link out to."
    )


class CardGridBlock(blocks.StructBlock):
    cards = blocks.ListBlock(CardGrid(), help_text="Please use a minimum of 2 cards.")

    class Meta:
        icon = "placeholder"
        template = "fragments/blocks/card_grid_block.html"
