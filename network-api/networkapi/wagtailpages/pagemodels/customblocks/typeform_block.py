from wagtail.core import blocks


class TypeFormBlock(blocks.StructBlock):
    url = blocks.URLBlock(
        help_text="The URL of the published typeform"
    )

    height = blocks.IntegerBlock(
        default=500,
        help_text="The height of the view on a desktop"
    )

    class Meta:
        icon = 'placeholder'
        template = 'wagtailpages/blocks/typeform_block.html'
