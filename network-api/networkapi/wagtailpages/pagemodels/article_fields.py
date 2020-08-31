"""
Article StreamBlocks
"""
from . import customblocks
from wagtail.core import blocks


article_fields = [
    ('content', customblocks.ArticleRichText(
        features=['bold' ,'italic', 'h3', 'ol', 'ul', 'image', 'footnotes'],
    )),
    ('callout', blocks.BlockQuoteBlock(
        template="wagtailpages/blocks/article_blockquote_block.html"
    )),
]
