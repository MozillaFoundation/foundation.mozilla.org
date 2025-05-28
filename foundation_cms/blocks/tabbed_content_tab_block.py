from wagtail import blocks
from .text_image_block import TextImageBlock
from .tab_card_set_block import TabCardSetBlock
from foundation_cms.base.models.base_block import BaseBlock


class TabbedContentTabBlock(BaseBlock):
    title = blocks.CharBlock(required=True, help_text="Title shown on the tab button")
    subtitle = blocks.CharBlock(required=False, help_text="Subtitle shown under the title on the tab")
    content = blocks.StreamBlock(
        [
            ("rich_text", blocks.RichTextBlock()),
            ("text_image", TextImageBlock()),
            ("tab_card_set", TabCardSetBlock()),
        ],
        required=True,
        min_num=1,
        help_text="Add one or more content blocks to the tab."
    )

    class Meta:
        icon = "form"
        label = "Tab"
