from wagtail import blocks

from networkapi.wagtailpages.pagemodels.customblocks.link_block import LinkBlock


class LinkButtonBlock(blocks.StructBlock):
    label = blocks.CharBlock()

    # We use a char block because UrlBlock does not
    # allow for relative linking.
    URL = blocks.CharBlock()

    target = LinkBlock(label="")

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
