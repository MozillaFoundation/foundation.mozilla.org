from wagtail import blocks

from foundation_cms.legacy_cms.wagtailpages.pagemodels.customblocks.link_block import LinkBlock


class LinkButtonBlock(LinkBlock):
    # Buttons can have different looks, so we
    # offer the choice to decide which styling
    # should be used.
    styling = blocks.ChoiceBlock(
        choices=[
            ("btn-primary", "Primary button"),
            ("btn-secondary", "Secondary button"),
        ],
        default="btn-primary",
    )

    class Meta:
        icon = "link"
        template = "wagtailpages/blocks/link_button_block.html"
