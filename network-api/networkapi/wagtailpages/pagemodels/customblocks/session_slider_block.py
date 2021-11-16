from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtailmedia.blocks import VideoChooserBlock

from .common.link_blocks import (
    InternalLinkBlock,
    ExternalLinkBlock,
    LabelledExternalLinkBlock,
    LabelledInternalLinkBlock,
)


class SessionItemBlock(blocks.StructBlock):
    title = blocks.CharBlock(help_text='Heading for the card.')

    author_subheading = blocks.CharBlock(required=False, help_text='Author of this session.')

    image = ImageChooserBlock(help_text='The image associated with this session.')

    body = blocks.RichTextBlock(help_text='Body text of this card.')

    video = VideoChooserBlock(
        required=False,
        help_text='Video that will autoplay when this card is hovered on',
    )

    link = blocks.StreamBlock(
        [
            ('internal', InternalLinkBlock()),
            ('external', ExternalLinkBlock()),
        ],
        help_text='Page or external URL this card will link out to.',
        max_num=1,
    )


class SessionSliderBlock(blocks.StructBlock):
    title = blocks.CharBlock(help_text='Heading for the slider.')

    session_items = blocks.StreamBlock(
        [
            ('session_item', SessionItemBlock()),
        ],
        help_text='A list of sessions in the slider.',
    )

    button = blocks.StreamBlock(
        [
            ('internal', LabelledInternalLinkBlock()),
            ('external', LabelledExternalLinkBlock()),
        ],
        help_text='Button that appears below the slider.',
        required=False,
        max_num=1,
    )

    class Meta:
        icon = 'list-ul'
        help_text = 'Recommendation: No more than 5 items should be in this slider.'
        template = 'wagtailpages/blocks/session_slider_block.html'
