from wagtail import blocks

from .link_button_block import LinkButtonBlock


class CTAAsideBlock(blocks.StructBlock):
    title = blocks.CharBlock(help_text="Heading for the card.")
    body = blocks.TextBlock(help_text="Body text of the card.")
    button = LinkButtonBlock()

    class Meta:
        template = "wagtailpages/blocks/cta_aside_block.html"
        block_counts = {
            "content": {"max_num": 1, "min_num": 1},
            "button": {"max_num": 1, "min_num": 1},
        }
