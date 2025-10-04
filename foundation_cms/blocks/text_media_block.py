from wagtail import blocks

from foundation_cms.base.models.base_block import BaseBlock

from .link_block import OptionalLinkBlock
from .media_block import CustomMediaBlock


class TextMediaBlock(BaseBlock):
    """
    A flexible Text + Media block with an optional title, subtitle, body text,
    media, and link. This is the base variant used site-wide.
    """

    title = blocks.CharBlock(required=False)
    subtitle = blocks.CharBlock(required=False)
    text = blocks.RichTextBlock(required=False)
    media = CustomMediaBlock(required=False)
    link = OptionalLinkBlock(required=False)

    class Meta:
        icon = "image"
        label = "Text & Media"
        template_name = "text_media_block.html"


class NarrowTextMediaBlock(TextMediaBlock):
    """
    A narrower variant of TextMediaBlock, currently used only on the NP Homepage.

    Notes:
        - NP Homepage needs something separate in case Text & Media block is used later.
        - We don’t foresee needing this narrower layout elsewhere right now.
        - If variants expand in the future, consider refactoring into a single
          TextMediaBlock with a `ChoiceBlock` for style/variant selection.
    """

    class Meta:
        icon = "image"
        label = "Text & Media (Narrow)"
        template_name = "text_media_block__narrow.html"
