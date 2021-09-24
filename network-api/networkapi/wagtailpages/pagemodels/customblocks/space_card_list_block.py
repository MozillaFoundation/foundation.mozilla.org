from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class SpaceCardBlockStructValue(blocks.StructValue):
    @property
    def link_url(self):
        block = self.get('link')[0]

        if block.block_type == 'internal':
            return block.value.url
        elif block.block_type == 'external':
            return block.value

        return ''


class SpaceCardBlock(blocks.StructBlock):
    image = ImageChooserBlock()

    title = blocks.CharBlock(
        help_text='Heading for the card.'
    )

    body = blocks.TextBlock(
        help_text='Body text of the card.'
    )

    link = blocks.StreamBlock(
        [
            ('internal', blocks.PageChooserBlock(help_text='Page that this card should link out to.')),
            ('external', blocks.URLBlock(help_text='URL that this card should link out to.')),
        ],
        max_num=1,
    )

    class Meta:
        value_class = SpaceCardBlockStructValue


class SpaceCardListBlock(blocks.StructBlock):
    title = blocks.CharBlock()

    space_cards = blocks.ListBlock(SpaceCardBlock())

    class Meta:
        icon = 'placeholder'
        template = 'wagtailpages/blocks/space_card_list_block.html'
