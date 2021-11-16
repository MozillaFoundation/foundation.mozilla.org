from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock

from .common.link_blocks import InternalLinkBlock, ExternalLinkBlock


class SpacesCardBlock(blocks.StructBlock):
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
        label = 'Spaces Card'


class SpacesBlock(blocks.StructBlock):
    title = blocks.CharBlock()

    cards = blocks.StreamBlock(
        [
            ('space_card', SpacesCardBlock()),
        ],
        help_text='A list of Spaces Cards.',
    )

    class Meta:
        icon = 'placeholder'
        template = 'wagtailpages/blocks/spaces_block.html'
