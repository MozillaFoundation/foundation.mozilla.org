from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

from networkapi.wagtailpages.pagemodels.customblocks.link_block import (
    LinkWithoutLabelBlock,
)


class GroupListingCard(blocks.StructBlock):
    image = ImageChooserBlock()

    alt_text = blocks.CharBlock(required=False, help_text="Alt text for card's image.")

    meta_data = blocks.CharBlock(help_text="Optional meta data information for the card.", required=False)

    title = blocks.CharBlock(help_text="Heading for the card.")

    body = blocks.RichTextBlock(features=["bold", "link"], help_text="Body text of the card.")
    url = blocks.CharBlock(required=False, help_text="The URL this card should link to.")
    link = blocks.ListBlock(
        LinkWithoutLabelBlock(), min_num=0, max_num=1, help_text="Optional link that this card should link to."
    )


class GroupListingBlock(blocks.StructBlock):
    title = blocks.CharBlock(help_text="Heading for the group of cards.", required=False)
    cards = blocks.ListBlock(
        GroupListingCard(),
    )

    class Meta:
        icon = "placeholder"
        template = "wagtailpages/blocks/group_listing_block.html"
