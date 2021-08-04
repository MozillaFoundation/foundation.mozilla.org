"""
Article StreamBlocks
"""
from . import customblocks
from wagtail.core import blocks
from wagtail.contrib.table_block.blocks import TableBlock

article_fields = [
    ('airtable', customblocks.AirTableBlock()),
    ('callout', blocks.BlockQuoteBlock(
        template="wagtailpages/blocks/article_blockquote_block.html"
    )),
    ('content', customblocks.ArticleRichText(
        features=['bold', 'italic', 'h2', 'h3', 'h4', 'h5', 'link', 'large', 'ol', 'ul', 'image', 'hr', 'footnotes'],
    )),
    ('image', customblocks.ArticleImageBlock()),
    ('double_image', customblocks.ArticleDoubleImageBlock()),
    ('full_width_image', customblocks.ArticleFullWidthImageBlock()),
    ('iframe', customblocks.iFrameBlock()),
    ('single_quote', customblocks.SingleQuoteBlock()),
    ('table', TableBlock(
        template="wagtailpages/blocks/article_table_block.html"
    )),
    ('video', customblocks.VideoBlock()),
    ('advanced_table', customblocks.AdvancedTableBlock()),
]
