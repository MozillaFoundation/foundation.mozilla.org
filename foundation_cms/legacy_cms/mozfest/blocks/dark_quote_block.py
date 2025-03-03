from foundation_cms.legacy_cms.wagtailpages.pagemodels.customblocks import single_quote_block


class DarkSingleQuoteBlock(single_quote_block.SingleQuoteBlock):
    # This inherits SingleQuoteBlock from
    # wagtailpages.pagemodels.customblocks.single_quote_block.py
    # so we can override the template to have a dark background.

    class Meta:
        template = "fragments/blocks/dark_quote_block.html"
        icon = "openquote"
        help_text = "A single quote block on a dark background"
