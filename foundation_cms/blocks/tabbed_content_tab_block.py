from wagtail import blocks
from foundation_cms.base.models.base_block import BaseBlock

class TabbedContentTabBlock(BaseBlock):
    title = blocks.CharBlock(required=True, help_text="Title shown on the tab button")
    subtitle = blocks.CharBlock(required=False, help_text="Subtitle shown under the title on the tab")
    content = blocks.StreamBlock(
        [
            ("rich_text", blocks.RichTextBlock()),
            # TODO add other blocks as they're built
        ],
        required=True,
        min_num=1,
        max_num=1,
        help_text="Only one content block per tab."
    )

    class Meta:
        icon = "form"
        label = "Tab"