from wagtail.core import blocks


class SingleQuoteBlock(blocks.StructBlock):

    quote = blocks.CharBlock()
    attribution = blocks.CharBlock(required=False)

    class Meta:
        template = 'wagtailpages/blocks/single_quote_block.html'
        icon = 'openquote'
        help_text = 'A single quote block'
