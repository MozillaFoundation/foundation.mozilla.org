"""
Article StreamBlocks
"""
from . import customblocks
from wagtail.core import blocks


article_fields = [
    ('content', customblocks.ArticleRichText(
        features=['bold' ,'italic', 'h3', 'ol', 'ul', 'image', 'footnotes'],
    )),
]
