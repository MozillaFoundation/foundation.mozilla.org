from wagtail import blocks

from legacy_cms.wagtailpages.pagemodels.customblocks.link_block import LinkBlock


class CTABlock(LinkBlock):
    heading = blocks.CharBlock(required=False)
    text = blocks.CharBlock(required=False)
    dark_background = blocks.BooleanBlock(required=False)

    class Meta:
        template = "fragments/blocks/cta_block.html"
        label = "Call to action"
