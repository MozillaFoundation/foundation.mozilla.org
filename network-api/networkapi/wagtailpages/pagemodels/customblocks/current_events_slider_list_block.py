from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock

from .common.link_blocks import LabelledExternalLinkBlock, LabelledInternalLinkBlock, LabelledDocumentLinkBlock


class CurrentEventBlock(blocks.StructBlock):
    title = blocks.CharBlock(help_text='Heading of the card.')

    subheading_link = blocks.StreamBlock(
        [
            ('internal', LabelledInternalLinkBlock()),
            ('external', LabelledExternalLinkBlock()),
        ],
        help_text='The link that appears below the card heading.',
        max_num=1,
        required=False,
    )

    image = ImageChooserBlock(help_text='The image associated with this event.')

    body = blocks.TextBlock(help_text='Body text of the card.')

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
    )

    class Meta:
        icon = 'form'
        label = 'Current Event Item'


class BlockSizeProperty(blocks.StructValue):
    def block_size(self):
        return 'wide'


class CurrentEventsSliderListBlock(blocks.StructBlock):
    title = blocks.CharBlock(help_text='Heading for the slider.')

    current_events = blocks.ListBlock(CurrentEventBlock(), help_text='A list of current events in the slider.')

    class Meta:
        icon = 'list-ul'
        help_text = 'Recommendation: No more than 5 items should be in this slider.'
        template = 'wagtailpages/blocks/current_events_slider_list_block.html'
        value_class = BlockSizeProperty
