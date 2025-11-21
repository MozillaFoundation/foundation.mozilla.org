from wagtail import blocks

from foundation_cms.base.models.base_block import BaseBlock

from .custom_rich_text_block import CustomRichTextBlock
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
    text = CustomRichTextBlock(required=False, label="Text")
    image = CustomImageBlock(required=False)
    link = OptionalLinkBlock(required=False)

    class Meta:
        icon = "image"
        label = "Text & Image"
        template_name = "text_image_block.html"


class TextMediaBlock(TextImageBlock):
    """
    A variant of TextImageBlock with video support, currently used only on the NP Homepage.

    Notes:
        - NP Homepage needs something separate in case Text & Image block is used later.
        - We don’t foresee needing this layout elsewhere right now.
        - If variants expand in the future, consider refactoring into a single
          TextImageBlock with a `ChoiceBlock` for style/variant selection.
    """

    background_color = blocks.ChoiceBlock(
        choices=[
            ("white", "White"),
            ("neutral-100", "Grey 100"),
            ("neutral-200", "Grey 200"),
            ("neutral-300", "Grey 300"),
            ("blue-100", "Blue 100"),
            ("blue-200", "Blue 200"),
            ("blue-300", "Blue 300"),
            ("green-100", "Green 100"),
            ("green-200", "Green 200"),
            ("green-300", "Green 300"),
            ("orange-100", "Orange 100"),
            ("orange-200", "Orange 200"),
            ("orange-300", "Orange 300"),
            ("yellow-100", "Yellow 100"),
            ("yellow-200", "Yellow 200"),
            ("yellow-300", "Yellow 300"),
        ],
        default="white",
    )
    media = CustomMediaBlock(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.child_blocks.pop("image", None)

    class Meta:
        icon = "image"
        label = "Text & Media"
        template_name = "text_media_block.html"
