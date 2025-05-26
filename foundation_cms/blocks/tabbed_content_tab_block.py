from wagtail import blocks
from foundation_cms.base.models.base_block import BaseBlock
from wagtail.images.blocks import ImageBlock


class TabImageBlock(blocks.StructBlock):
    image = ImageBlock(required=True)

    class Meta:
        icon = "image"
        template = "patterns/blocks/image_block.html"


class TabbedContentTabBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, help_text="Title shown on the tab button")
    subtitle = blocks.CharBlock(required=False, help_text="Subtitle shown under the title on the tab")
    content = blocks.StreamBlock(
        [
            ("rich_text", blocks.RichTextBlock()),
            ("image", TabImageBlock()),
            # TODO add other blocks as they're built
        ],
        required=True,
        min_num=1,
        help_text="Add one or more content blocks to the tab."
    )

    class Meta:
        icon = "form"
        label = "Tab"
