from wagtail import blocks

from networkapi.wagtailpages.pagemodels.customblocks.link_block import LinkBlock


class CTABlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=False)
    text = blocks.CharBlock(required=False)
    target = LinkBlock()
    dark_background = blocks.BooleanBlock(required=False)

    class Meta:
        template = "fragments/blocks/cta_block.html"
        label = "Call to action"
