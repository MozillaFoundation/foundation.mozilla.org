from wagtail import blocks


class SingleQuoteBlock(blocks.StructBlock):
    quote = blocks.RichTextBlock(features=["bold"])
    attribution = blocks.CharBlock(required=False)
    attribution_info = blocks.RichTextBlock(required=False, features=["bold", "link", "large"])

    class Meta:
        template = "wagtailpages/blocks/single_quote_block.html"
        icon = "openquote"
        help_text = "A single quote block"
