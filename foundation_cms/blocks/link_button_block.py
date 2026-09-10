from wagtail import blocks

from foundation_cms.base.models.base_block import BaseBlock
from foundation_cms.blocks.link_block import LinkBlock


class BaseLinkButtonBlock(BaseBlock, LinkBlock):
    """A link rendered as a button, without any alignment control."""

    style = blocks.ChoiceBlock(
        choices=[
            ("btn-primary", "Primary"),
            ("btn-secondary", "Secondary"),
        ],
        default="btn-primary",
    )

    class Meta:
        icon = "link"
        template_name = "link_button_block.html"


class LinkButtonBlock(BaseLinkButtonBlock):
    """The default link button, with an editor-facing alignment control."""

    alignment = blocks.ChoiceBlock(
        choices=[
            ("link-button-block--left", "Left"),
            ("link-button-block--center", "Center"),
        ],
        default="link-button-block--left",
    )


class FixedAlignmentLinkButtonBlock(BaseLinkButtonBlock):
    """A link button whose position is decided by its container, not by the editor."""
