from wagtail import blocks

from foundation_cms.base.models.base_block import BaseBlock
from foundation_cms.blocks.link_block import LinkBlock


class LinkButtonBlock(BaseBlock, LinkBlock):

    style = blocks.ChoiceBlock(
        choices=[
            ("btn-primary", "Primary"),
            ("btn-secondary", "Secondary"),
        ],
        default="btn-primary",
    )
    alignment = blocks.ChoiceBlock(
        choices=[
            ("link-button-block--left", "Left"),
            ("link-button-block--center", "Center"),
        ],
        default="link-button-block--left",
    )

    class Meta:
        icon = "link"
        template_name = "link_button_block.html"


class NoticeBannerLinkButtonBlock(LinkButtonBlock):
    """
    LinkButtonBlock without the alignment dropdown, for the NoticeBanner snippet.
    """

    def __init__(self, local_blocks=None, **kwargs):
        super().__init__(local_blocks, **kwargs)
        self.child_blocks.pop("alignment", None)
