from wagtail.core import blocks


class AsideBlock(blocks.StructBlock):
    class Meta:
        icon = 'placeholder'
        template = 'wagtailpages/blocks/aside.html'

    title = blocks.CharBlock(
        help_text='Heading for the card.',
        required=False
    )

    body = blocks.TextBlock(
        help_text='Body text of the card.',
        required=False
    )
