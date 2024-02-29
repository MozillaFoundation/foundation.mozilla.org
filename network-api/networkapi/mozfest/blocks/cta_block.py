from wagtail import blocks

from networkapi.wagtailpages.pagemodels.customblocks.link_block import LinkBlock


class CTABlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=False)
    text = blocks.CharBlock(required=False)
    link_url = blocks.URLBlock(required=False)
    link_text = blocks.CharBlock(required=False, max_length=50)
    target = LinkBlock()
    dark_background = blocks.BooleanBlock(required=False)

    class Meta:
        template = "fragments/blocks/cta_block.html"
        label = "Call to action"
