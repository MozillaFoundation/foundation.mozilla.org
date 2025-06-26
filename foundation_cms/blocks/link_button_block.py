from foundation_cms.blocks.link_block import LinkBlock
from foundation_cms.base.models.base_block import BaseBlock


class LinkButtonBlock(BaseBlock, LinkBlock):

    # TODO: Uncomment the lines below to enable styling for buttons, once
    # we get the OK from the design team.

    # Buttons can have different looks, so we
    # offer the choice to decide which styling
    # should be used.
    # styling = blocks.ChoiceBlock(
    #     choices=[
    #         ("btn-primary", "Primary button"),
    #         ("btn-secondary", "Secondary button"),
    #     ],
    #     default="btn-primary",
    # )

    class Meta:
        icon = "link"
        template_name = "link_button_block.html"
