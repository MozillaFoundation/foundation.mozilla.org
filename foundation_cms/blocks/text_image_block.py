from wagtail import blocks

from foundation_cms.base.models.base_block import BaseBlock

from .image_block import CustomImageBlock
from .link_block import OptionalLinkBlock
from .media_block import CustomMediaBlock


class TextImageBlock(BaseBlock):
    """
    A flexible Text + Image block with an optional title, subtitle, body text,
    image, and link. This is the base variant used site-wide.
    """

    title = blocks.CharBlock(required=False)
    subtitle = blocks.CharBlock(required=False)
    text = blocks.RichTextBlock(required=False)
    image = CustomImageBlock(required=False)
    link = OptionalLinkBlock(required=False)

    class Meta:
        icon = "image"
        label = "Text & Image"
        template_name = "text_media_block.html"


class TextMediaBlock(TextImageBlock):
    """
    A variant of TextImageBlock with video support, currently used only on the NP Homepage.

    Notes:
        - NP Homepage needs something separate in case Text & Image block is used later.
        - We don’t foresee needing this layout elsewhere right now.
        - If variants expand in the future, consider refactoring into a single
          TextImageBlock with a `ChoiceBlock` for style/variant selection.
    """

    media = CustomMediaBlock(required=False)
    image = None

    class Meta:
        icon = "image"
        label = "Text & Media"
        template_name = "text_media_block.html"
