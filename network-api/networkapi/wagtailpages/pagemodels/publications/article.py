
from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.core.models import Orderable, Page
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, StreamFieldPanel
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from networkapi.wagtailpages.models import BlogAuthor
from ..mixin.foundation_metadata import FoundationMetadataPageMixin
from ..article_fields import article_fields

"""
TODO:
agree on featureset for content
callout may have different featureset, but we mainly want the ability to distinguish it for styling?
it was implied we might want to include links/call to actions in a callout, but maybe that would not be good,
in which case we could just use a BlockQuoteBlock
"""


class ArticleAuthors(Orderable):
    """This allows us to select one or more blog authors from Snippets."""

    page = ParentalKey("wagtailpages.ArticlePage", related_name="authors")
    author = models.ForeignKey(
        BlogAuthor,
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )

    panels = [
        SnippetChooserPanel("author"),
    ]

    def __str__(self):
        return self.author.name


class ArticlePage(FoundationMetadataPageMixin, Page):

    """

    Article belong to PublicationPages
    An Article can only belong to one Chapter/Publication Page
    An ArticlePage can have no children

    ? If these only belong to PublicationPages, should be extra explicit and call it PublicationArticlePage?
    """
    parent_page_types = ['PublicationPage']
    subpage_types = []
    body = StreamField(article_fields)

    sidebar_summary_title = models.CharField(
        blank=True,
        default="Article Summary",
        max_length=250,
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            InlinePanel("authors", label="Author", min_num=0)
        ], heading="Author(s)"),
        StreamFieldPanel('body'),
        InlinePanel("footnotes", label="Footnotes"),
        FieldPanel('sidebar_summary_title'),
    ]
