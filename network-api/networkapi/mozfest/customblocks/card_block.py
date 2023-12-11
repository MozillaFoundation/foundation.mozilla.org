from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

"""
The following card and grid definitions are specifically for Mozfest.
They are based on wagtailpages.pagemodels.customblocks.card_grid.py
but have been modified to fit the Mozfest design.
"""


class MozfestCardGrid(blocks.StructBlock):
    image = ImageChooserBlock()

    alt_text = blocks.CharBlock(required=False, help_text="Alt text for card's image.")

    title = blocks.CharBlock(help_text="Heading for the card.")

    body = blocks.TextBlock(help_text="Body text of the card.", required=False)

    link_url = blocks.CharBlock(
        required=False,
        help_text="Optional URL that this card should link out to. " "(Note: If left blank, link will not render.) ",
    )

    link_label = blocks.CharBlock(
        required=False,
        help_text="Optional Label for the URL link above. " "(Note: If left blank, link will not render.) ",
    )


class MozfestCardGridBlock(blocks.StructBlock):
    heading = blocks.CharBlock(help_text="Heading for the block.")
    cards = blocks.ListBlock(MozfestCardGrid(), help_text="Please use a minimum of 2 cards.")

    class Meta:
        icon = "placeholder"
        template = "fragments/blocks/mozfest_card_grid_block.html"
        label = "Mozfest Card Grid"
