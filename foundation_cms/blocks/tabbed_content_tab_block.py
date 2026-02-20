from wagtail import blocks

from .custom_rich_text_block import CustomRichTextBlock
from .tabbed_content_card_set_block import TabbedContentCardSetBlock
from .text_image_block import TextImageBlock


class TabbedContentTabBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, help_text="Title shown on the tab button")
    subtitle = blocks.CharBlock(required=False, help_text="Subtitle shown under the title on the tab")
    content = blocks.StreamBlock(
        [
            ("rich_text", CustomRichTextBlock()),
            ("text_image", TextImageBlock()),
            ("tab_card_set", TabbedContentCardSetBlock()),
        ],
        required=True,
        min_num=1,
        help_text="Add one or more content blocks to the tab.",
    )

    class Meta:
        icon = "form"
        label = "Tab"
