from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock

from .common.link_blocks import InternalLinkBlock, ExternalLinkBlock


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
            ('internal', InternalLinkBlock()),
            ('external', ExternalLinkBlock()),
        ],
        help_text='Page or external URL this card will link out to.',
        max_num=1,
    )

    class Meta:
        icon = 'form'
        label = 'Space Card'


class SpaceCardListBlock(blocks.StructBlock):
    title = blocks.CharBlock()

    space_cards = blocks.StreamBlock(
        [
            ('space_card', SpaceCardBlock()),
        ],
        help_text='A list of Space Cards.',
    )

    class Meta:
        icon = 'placeholder'
        template = 'wagtailpages/blocks/space_card_list_block.html'
