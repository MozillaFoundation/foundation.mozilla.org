from wagtail import blocks

from foundation_cms.legacy_cms.wagtailpages.pagemodels.customblocks.link_block import (
    LinkWithoutLabelBlock,
)


class TextOnlyTeaserCard(blocks.StructBlock):
    heading = blocks.CharBlock(help_text="Heading for the card.")
    link = blocks.ListBlock(
        LinkWithoutLabelBlock(), min_num=0, max_num=1, help_text="Optional link that the header should link out to."
    )
    meta_data = blocks.CharBlock(max_length=500)
    body = blocks.TextBlock(help_text="Body text of the card.", required=False, max_length=200)


class TextOnlyTeaserBlock(blocks.StructBlock):
    cards = blocks.ListBlock(TextOnlyTeaserCard(), help_text="Please use a minimum of 3 cards.", min_num=3)

    class Meta:
        icon = "placeholder"
        template = "wagtailpages/blocks/text_only_teaser_block.html"
