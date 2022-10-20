from wagtail.core import blocks


class TextOnlyTeaserCard(blocks.StructBlock):

    heading = blocks.CharBlock(
        help_text='Heading for the card.'
    )
    heading_link = blocks.PageChooserBlock(
        required=False,
        help_text='Page that the header should link out to.'
    )
    meta_data = blocks.CharBlock(
        max_length=500
    )
    body = blocks.TextBlock(
        help_text='Body text of the card.',
        required=False,
        max_length=200
    )


class TextOnlyTeaserBlock(blocks.StructBlock):
    cards = blocks.ListBlock(
        TextOnlyTeaserCard(),
        help_text="Please use a minimum of 3 cards.",
        min_num=3
    )

    class Meta:
        icon = 'placeholder'
        template = 'wagtailpages/blocks/text_only_teaser_block.html'
