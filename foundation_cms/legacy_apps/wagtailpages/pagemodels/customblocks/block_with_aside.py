from wagtail import blocks

from .aside_fields import aside_fields
from .full_content_rich_text_options import full_content_rich_text_options
from .listing import ListingBlock


class BlockWithAside(blocks.StructBlock):
    content = blocks.StreamBlock(
        [
            ("listing", ListingBlock()),
            (
                "paragraph",
                blocks.RichTextBlock(features=full_content_rich_text_options),
            ),
        ],
        max_num=1,
        help_text="The wider block that appears on the left on desktop",
        icon="doc-full",
    )

    aside = blocks.StreamBlock(
        aside_fields,
        required=False,
        icon="doc-full",
        help_text="Elements here will appear in the column on the right side of the page on desktop. "
        "This can be left blank if you would just like a 2/3 column on the left",
    )

    class Meta:
        icon = "pick"
        template = "wagtailpages/blocks/block_with_aside.html"
