from wagtail.core import blocks


class QuoteBlock(blocks.StructBlock):

    # The goal is to be able to cycle through multiple quotes,
    # so let's accept multiple quotes to start even if we only show one for now.
    # This way we don't have to migrate the model again later

    quotes = blocks.ListBlock(blocks.StructBlock([
    ('quote', blocks.RichTextBlock(features=['bold'])),
        ('attribution', blocks.CharBlock(required=False))
    ]))

    class Meta:
        template = 'wagtailpages/blocks/quote_block.html'
        icon = 'openquote'
        help_text = 'Multiple quotes can be entered, but for now we are only using the first'
