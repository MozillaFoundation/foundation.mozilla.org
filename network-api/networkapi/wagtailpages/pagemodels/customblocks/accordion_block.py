from wagtail.core import blocks
from ..customblocks.base_rich_text_options import base_rich_text_options
from .datawrapper_block import DatawrapperBlock
from .image_block import ImageBlock

accordion_rich_text = blocks.RichTextBlock(
    features=base_rich_text_options + ['ul', 'ol', 'document-link'],
    blank=True
)


class AccordionBlock(blocks.StructBlock):

    title = blocks.CharBlock(
        help_text='Heading for the Accordion.'
    )

    accordion_items = blocks.StreamBlock(
            [
                ('rich_text', accordion_rich_text),
                ('datawrapper', DatawrapperBlock()),
                ('image', ImageBlock())
            ]
        )

    class Meta:

        icon = 'placeholder'
        template = 'wagtailpages/blocks/accordion_block.html'
