from wagtail.core import blocks


class AirTableBlock(blocks.StructBlock):
    url = blocks.URLBlock(
        help_text="Copied from the Airtable embed code. The word 'embed' will be in the url"
    )
    height = blocks.IntegerBlock(
        default=533,
        help_text=" The pixel height on desktop view, usually copied from the Airtable embed code",
    )

    class Meta:
        icon = 'placeholder'
        template = 'wagtailpages/blocks/airtable_block.html'
