
from bs4 import BeautifulSoup
from django.db import models
from django.utils.text import slugify
from modelcluster.fields import ParentalKey

from wagtail.core.models import Orderable, Page
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import InlinePanel, MultiFieldPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from networkapi.wagtailpages.models import BlogAuthor, PublicationPage
from ..mixin.foundation_metadata import FoundationMetadataPageMixin
from ..article_fields import article_fields


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

    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Publication Hero Image',
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            InlinePanel("authors", label="Author", min_num=0)
        ], heading="Author(s)"),
        MultiFieldPanel([
            ImageChooserPanel("hero_image"),
        ], heading="Hero"),
        StreamFieldPanel('body'),
        InlinePanel("footnotes", label="Footnotes"),
    ]

    @property
    def next_page(self):
        # Try to get the next sibling page.
        try:
            next_page = self.get_siblings().filter(path__gt=self.path, live=True)[0]
        except IndexError:
            next_page = self.get_parent()
        return next_page

    @property
    def prev_page(self):
        # Try to get the prev sibling page.
        try:
            prev_page = self.get_siblings().filter(path__lt=self.path, live=True).reverse()[0]
        except IndexError:
            prev_page = self.get_parent()
        return prev_page

    def get_titles(self):
        body = self.body.__dict__['stream_data']
        headers = []
        for block in body:
            if block['type'] == "content":
                soup = BeautifulSoup(block['value'], 'html.parser')
                _headers = soup.findAll('h2')
                for _h in _headers:
                    headers.append(_h.contents[0])
        data = {
            slugify(header): header for header in headers
        }
        return tuple(data.items())

    def breadcrumb_list(self):
        """
        Get all the parent PublicationPages and return a QuerySet
        """
        return Page.objects.ancestor_of(self).type(PublicationPage).live()
