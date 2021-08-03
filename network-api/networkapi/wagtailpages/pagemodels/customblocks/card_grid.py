from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class CardGrid(blocks.StructBlock):
    image = ImageChooserBlock()

    title = blocks.CharBlock(
        help_text='Heading for the card.'
    )

    body = blocks.TextBlock(
        help_text='Body text of the card.'
    )

    link_url = blocks.CharBlock(
        help_text='URL that this card should link out to.',
    )

    link_label = blocks.CharBlock(
        help_text='Label for the URL link above.',
    )


class CardGridBlock(blocks.StructBlock):
    grid_items = blocks.ListBlock(CardGrid())

    class Meta:

        icon = 'placeholder'
        template = 'wagtailpages/blocks/card_grid_block.html'
