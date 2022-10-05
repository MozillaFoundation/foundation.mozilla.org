from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class ListingCard(blocks.StructBlock):
    image = ImageChooserBlock()

    alt_text = blocks.CharBlock(
        required=False,
        help_text='Alt text for card\'s image.'
    )

    title = blocks.CharBlock(
        help_text='Heading for the card.'
    )

    body = blocks.RichTextBlock(
        features=['bold'],
        help_text='Body text of the card.'
    )

    link = blocks.PageChooserBlock(
        required=False,
        help_text='Page that this should link out to.'
    )


class ListingBlock(blocks.StructBlock):
    cards = blocks.ListBlock(
        ListingCard(),
        help_text="Please use a minimum of 2 cards.",
        min_num=2
    )

    class Meta:

        icon = 'placeholder'
        template = 'wagtailpages/blocks/listing_block.html'
