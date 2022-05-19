from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
from ..customblocks.base_rich_text_options import base_rich_text_options

from .common.link_blocks import LabelledExternalLinkBlock, LabelledInternalLinkBlock, LabelledDocumentLinkBlock


class SlideBlock(blocks.StructBlock):
    title = blocks.CharBlock(help_text='Heading of the card.', required=False)

    image = ImageChooserBlock(help_text='The image associated with this event.')

    caption = blocks.TextBlock(help_text='Caption for slider image', required=False)

    body = blocks.RichTextBlock(
        features=base_rich_text_options + ['large'],
        blank=True,
        required=False
    )

    buttons = blocks.StreamBlock(
        [
            ('internal', LabelledInternalLinkBlock()),
            ('external', LabelledExternalLinkBlock()),
            ('document', LabelledDocumentLinkBlock(
                help_text='An iCal document can be attached here for an "Add to Calendar" button.'
            )),
        ],
        help_text='A list of buttons that will appear at the bottom of the card.',
        max_num=2,
        required=False
    )

    class Meta:
        icon = 'form'
        label = 'Current Slide Item'


class FoundationSliderBlock(blocks.StructBlock):
    title = blocks.CharBlock(help_text='Heading for the slider.', required=False)

    slides = blocks.StreamBlock(
        [
            ('slide', SlideBlock()),
        ],
        help_text='A list of slides.',
    )

    class Meta:
        icon = 'list-ul'
        help_text = (
            'Recommendation: No more than 5 items should be in this slider. '
            'This slider cannot be placed at the top of the page when a signup form is present as they will overlap.'
        )
        template = 'wagtailpages/blocks/foundation_slider_block.html'
