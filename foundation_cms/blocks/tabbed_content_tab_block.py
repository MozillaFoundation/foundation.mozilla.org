from wagtail import blocks
from .text_image_block import TextImageBlock
from .tabbed_content_card_set_block import TabbedContentCardSetBlock

class TabbedContentTabBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, help_text="Title shown on the tab button")
    subtitle = blocks.CharBlock(required=False, help_text="Subtitle shown under the title on the tab")
    content = blocks.StreamBlock(
        [
            ("rich_text", blocks.RichTextBlock()),
            ("text_image", TextImageBlock()),
            ("tab_card_set", TabbedContentCardSetBlock()),
        ],
        required=True,
        min_num=1,
        help_text="Add one or more content blocks to the tab."
    )

    class Meta:
        icon = "form"
        label = "Tab"
