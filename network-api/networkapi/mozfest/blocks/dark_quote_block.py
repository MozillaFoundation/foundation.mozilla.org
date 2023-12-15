from wagtail import blocks


class DarkSingleQuoteBlock(blocks.StructBlock):
    # This is a copy of the SingleQuoteBlock from
    # wagtailpages.pagemodels.customblocks.single_quote_block.py
    # There is obviously code duplication here, but it's necessary due to the
    # styling changes and the different template.
    # And explicit is better than implicit.
    quote = blocks.RichTextBlock(features=["bold"])
    attribution = blocks.CharBlock(required=False)
    attribution_info = blocks.RichTextBlock(required=False, features=["bold", "link", "large"])

    class Meta:
        template = "fragments/blocks/dark_quote_block.html"
        icon = "openquote"
        help_text = "A single quote block on a dark background"
