"""
Article StreamBlocks
"""
from . import customblocks
from .customblocks.base_rich_text_options import base_rich_text_options
from wagtail.core import blocks
from wagtail.contrib.table_block.blocks import TableBlock

article_fields = [
    ('airtable', customblocks.AirTableBlock()),
    ('callout', blocks.RichTextBlock(
        features=['bold'],
        template="wagtailpages/blocks/article_blockquote_block.html"
    )),
    ('card_grid', customblocks.CardGridBlock()),
    ('content', customblocks.ArticleRichText(
        features=base_rich_text_options + ['h2', 'h3', 'h4', 'h5', 'large', 'ol', 'ul', 'image', 'hr', 'footnotes'],
    )),
    ('image', customblocks.ArticleImageBlock()),
    ('double_image', customblocks.ArticleDoubleImageBlock()),
    ('full_width_image', customblocks.ArticleFullWidthImageBlock()),
    ('iframe', customblocks.iFrameBlock()),
    ('linkbutton', customblocks.LinkButtonBlock()),
    ('single_quote', customblocks.SingleQuoteBlock()),
    ('table', TableBlock(
        template="wagtailpages/blocks/article_table_block.html"
    )),
    ('video', customblocks.VideoBlock()),
    ('advanced_table', customblocks.AdvancedTableBlock()),
]
