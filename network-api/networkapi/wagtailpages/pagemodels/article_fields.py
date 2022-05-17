"""
Article StreamBlocks
"""
from . import customblocks
from .customblocks.full_content_rich_text_options import full_content_rich_text_options
from wagtail.core import blocks
from wagtail.contrib.table_block.blocks import TableBlock

article_fields = [
    ('accordion', customblocks.AccordionBlock()),
    ('airtable', customblocks.AirTableBlock()),
    ('datawrapper', customblocks.DatawrapperBlock()),
    ('callout', blocks.RichTextBlock(
        features=['bold'],
        template="wagtailpages/blocks/article_blockquote_block.html"
    )),
    ('card_grid', customblocks.CardGridBlock()),
    ('content', customblocks.ArticleRichText(
        features=full_content_rich_text_options + ['large', 'image', 'footnotes'],
    )),
    ('image', customblocks.ArticleImageBlock()),
    ('double_image', customblocks.ArticleDoubleImageBlock()),
    ('full_width_image', customblocks.ArticleFullWidthImageBlock()),
    ('iframe', customblocks.iFrameBlock()),
    ('linkbutton', customblocks.LinkButtonBlock()),
    ('single_quote', customblocks.SingleQuoteBlock()),
    ('slider', customblocks.FoundationSliderBlock()),
    ('table', TableBlock(
        template="wagtailpages/blocks/article_table_block.html"
    )),
    ('video', customblocks.VideoBlock()),
    ('advanced_table', customblocks.AdvancedTableBlock()),
]
