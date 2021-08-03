from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList

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
        help_text='URL that this card should link out to.',
    )

    link_label = blocks.CharBlock(
        help_text='Label for the URL link above.',
    )


class CardGridBlock(blocks.StructBlock):
    cards = blocks.ListBlock(CardGrid(), help_text="Please use a minimum of 2 cards.")
    


    class Meta:

        icon = 'placeholder'
        template = 'wagtailpages/blocks/card_grid_block.html'

        