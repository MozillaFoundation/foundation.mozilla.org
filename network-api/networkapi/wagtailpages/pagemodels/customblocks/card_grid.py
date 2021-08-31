from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class CardGrid(blocks.StructBlock):
    image = ImageChooserBlock()

    alt_text = blocks.CharBlock(
        required=False,
        help_text='Alt text for card\'s image.'
    )

    title = blocks.CharBlock(
        help_text='Heading for the card.'
    )

    body = blocks.TextBlock(
        help_text='Body text of the card.'
    )

    link_url = blocks.CharBlock(
        required=False,
        help_text='Optional URL that this card should link out to. '
                  '(Note: If left blank, link will not render.) ',
    )

    link_label = blocks.CharBlock(
        required=False,
        help_text='Optional Label for the URL link above. '
                  '(Note: If left blank, link will not render.) ',

    )


class CardGridBlock(blocks.StructBlock):
    cards = blocks.ListBlock(CardGrid(), help_text="Please use a minimum of 2 cards.")

    class Meta:

        icon = 'placeholder'
        template = 'wagtailpages/blocks/card_grid_block.html'
