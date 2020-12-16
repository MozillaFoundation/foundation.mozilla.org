from django.db import models
from modelcluster.fields import ParentalKey

from wagtail.core.models import Orderable, Page
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import InlinePanel, MultiFieldPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from networkapi.wagtailpages.models import BlogAuthor, PublicationPage
from networkapi.wagtailpages.utils import get_richtext_titles
from networkapi.wagtailpages.utils import set_main_site_nav_information
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
        next_page = self.get_siblings().filter(path__gt=self.path, live=True).first()
        if not next_page:
            next_page = self.get_parent()
        return next_page

    @property
    def prev_page(self):
        # Try to get the prev sibling page.
        prev_page = self.get_siblings().filter(path__lt=self.path, live=True).reverse().first()
        if not prev_page:
            prev_page = self.get_parent()
        return prev_page

    def breadcrumb_list(self):
        """
        Get all the parent PublicationPages and return a QuerySet
        """
        return Page.objects.ancestor_of(self).type(PublicationPage).live()

    @property
    def zen_nav(self):
        return True

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        # Add get_titles to the page context. This is in get_context() because
        # we need access to the `request` object
        # menu_items is required for zen_nav in the templates
        return set_main_site_nav_information(self, context, 'Homepage')
        context['get_titles'] = get_plaintext_titles(request, self.body, "content")
        return context
