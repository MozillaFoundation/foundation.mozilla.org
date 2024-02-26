from wagtail import blocks
from wagtail_link_block.blocks import LinkBlock as WagtailLinkBlock


class LinkBlock(blocks.StructBlock):
    label = blocks.CharBlock()
    link = WagtailLinkBlock()

    class Meta:
        icon = "link"
        template = "wagtailpages/blocks/link_block.html"
