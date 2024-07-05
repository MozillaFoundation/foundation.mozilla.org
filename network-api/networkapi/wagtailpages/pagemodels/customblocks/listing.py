from django.forms.utils import ErrorList
from wagtail import blocks
from wagtail.blocks.struct_block import StructBlockValidationError
from wagtail.images.blocks import ImageChooserBlock

from networkapi.wagtailpages.pagemodels.customblocks.link_block import (
    LinkWithoutLabelBlock,
)


class ListingCard(blocks.StructBlock):
    # Be mindful when extending or editing this class.
    # It is used in other places, like the MozFest Mixed Content block.
    # mozfest/blocks/mixd_content_block.py
    image = ImageChooserBlock()

    alt_text = blocks.CharBlock(required=False, help_text="Alt text for card's image.")

    title = blocks.CharBlock(help_text="Heading for the card.")
    highlighted_metadata = blocks.CharBlock(help_text="Metadata to highlight on the card.", required=False)
    metadata = blocks.CharBlock(help_text="Generic metadata.", required=False)

    body = blocks.RichTextBlock(features=["bold"], help_text="Body text of the card.", required=False)

    link = blocks.ListBlock(
        LinkWithoutLabelBlock(), min_num=0, max_num=1, help_text="Optional link that this card should link out to."
    )


class ListingBlock(blocks.StructBlock):
    heading = blocks.CharBlock(help_text="Heading for the block.", required=False)

    cards = blocks.ListBlock(ListingCard(), help_text="Please use a minimum of 2 cards.", min_num=2)

    cards_per_row = blocks.ChoiceBlock(
        choices=[(2, "2"), (3, "3")],
        default=2,
        required=False,
        help_text=(
            "Number of cards per row. Note: this is a max and fewer might be used if is less space is available."
        ),
    )

    class Meta:
        icon = "placeholder"
        template = "wagtailpages/blocks/listing_block.html"
