"""
Article StreamBlocks
"""
from . import customblocks
from wagtail.core import blocks
from wagtail.contrib.table_block.blocks import TableBlock

article_fields = [
    ('content', customblocks.ArticleRichText(
        features=['bold' ,'italic', 'h2', 'h3', 'h4', 'h5', 'large', 'ol', 'ul', 'image', 'hr', 'footnotes'],
    )),
    ('callout', blocks.BlockQuoteBlock(
        template="wagtailpages/blocks/article_blockquote_block.html"
    )),
    ('table', TableBlock(
        template="wagtailpages/blocks/article_table_block.html"
    )),
    ('double_image', customblocks.ArticleDoubleImageBlock()),
    ('full_width_image', customblocks.ArticleFullWidthImageBlock()),
]
