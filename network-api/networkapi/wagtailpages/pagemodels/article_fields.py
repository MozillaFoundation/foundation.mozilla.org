"""
Article StreamBlocks
"""

from wagtail import blocks
from wagtail.contrib.table_block.blocks import TableBlock

from . import customblocks
from .customblocks.base_rich_text_options import base_rich_text_options
from .customblocks.full_content_rich_text_options import full_content_rich_text_options

article_fields = [
    ("accordion", customblocks.AccordionBlock()),
    ("airtable", customblocks.AirTableBlock()),
    ("datawrapper", customblocks.DatawrapperBlock()),
    (
        "callout",
        blocks.RichTextBlock(
            features=base_rich_text_options + ["h2", "h3", "h4", "ul", "ol"],
            template="wagtailpages/blocks/article_blockquote_block.html",
        ),
    ),
    ("card_grid", customblocks.CardGridBlock()),
    (
        "content",
        customblocks.ArticleRichText(
            features=full_content_rich_text_options + ["large", "image", "footnotes"],
        ),
    ),
    ("image", customblocks.GeneralImageBlock()),
    ("image_grid", customblocks.ImageGridBlock()),
    ("image_text", customblocks.ImageTextBlock()),
    ("double_image", customblocks.ArticleDoubleImageBlock()),
    ("full_width_image", customblocks.ArticleFullWidthImageBlock()),
    ("iframe", customblocks.iFrameBlock()),
    ("linkbutton", customblocks.LinkButtonBlock()),
    ("single_quote", customblocks.SingleQuoteBlock()),
    ("slider", customblocks.FoundationSliderBlock()),
    ("spacer", customblocks.BootstrapSpacerBlock()),
    ("table", TableBlock(template="wagtailpages/blocks/article_table_block.html")),
    ("video", customblocks.VideoBlock()),
    ("advanced_table", customblocks.AdvancedTableBlock()),
]
