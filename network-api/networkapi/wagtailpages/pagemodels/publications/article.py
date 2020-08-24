
from django.db import models

from wagtail.core.models import Page
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.contrib.table_block.blocks import TableBlock

from ..mixin.foundation_metadata import FoundationMetadataPageMixin

"""
TODO: 
agree on featureset for content
callout may have different featureset, but we mainly want the ability to distinguish it for styling? 
it was implied we might want to include links/call to actions in a callout, but maybe that would not be good, 
in which case we could just use a BlockQuoteBlock
"""
article_blocks = [
    ('content', blocks.RichTextBlock()),
    ('callout', blocks.BlockQuoteBlock()),
    ('table', TableBlock()),
]


class ArticlePage(FoundationMetadataPageMixin, Page):

    """

    Article belong to PublicationPages
    An Article can only belong to one Chapter/Publication Page
    An ArticlePage can have no children

    ? If these only belong to PublicationPages, should be extra explicit and call it PublicationArticlePage?
    """
    parent_page_types = ['PublicationPage']
    subpage_types = []
    body = StreamField(article_blocks)

    sidebar_summary_title = models.CharField(
        blank=True,
        default="Article Summary",
        max_length=250,
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
        FieldPanel('sidebar_summary_title'),
    ]
