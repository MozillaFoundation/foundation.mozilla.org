from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock

from .link_blocks import LabelledExternalLinkBlock, LabelledInternalLinkBlock


class CurrentEventBlock(blocks.StructBlock):
    title = blocks.CharBlock('Heading for the card.')

    subheading_link = blocks.StreamBlock(
        [
            ('internal', LabelledInternalLinkBlock()),
            ('external', LabelledExternalLinkBlock()),
        ],
        max_num=1,
    )

    image = ImageChooserBlock()

    body = blocks.TextBlock(help_text='Body text of the card.')

    buttons = blocks.StreamBlock(
        [
            ('internal', LabelledInternalLinkBlock()),
            ('external', LabelledExternalLinkBlock()),
        ],
        max_num=2,
    )


class CurrentEventsSliderListBlock(blocks.StructBlock):
    title = blocks.CharBlock()

    current_events = blocks.ListBlock(CurrentEventBlock())

    class Meta:
        icon = 'list-ul'
        help_text = "Recommendation: No more than 5 items should be in this slider."
        template = 'wagtailpages/blocks/current_events_slider_list_block.html'
