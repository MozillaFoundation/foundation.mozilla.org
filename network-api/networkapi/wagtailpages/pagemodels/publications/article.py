from django.db import models
from modelcluster.fields import ParentalKey

from wagtail.core.models import Orderable, Page
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import InlinePanel, MultiFieldPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from networkapi.wagtailpages.models import BlogAuthor, PublicationPage
from networkapi.wagtailpages.utils import get_plaintext_titles
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
        """
        Get the next page for a publication. Details below:

        Check the parent page type. If the parent page type is a "Chapter Page",
        then look for siblings of `this` page. If no next sibling can be found
        look for the parent page next sibling. And if that cannot be found,
        return the Chapter Page's parent (Publication Page).
        Otherwise if the parent page is a Publication page: look for the next sibling,
        if there is no next sibling page, return this pages' parent.
        """

        parent = self.get_parent().specific
        next_page = self.get_siblings().filter(path__gt=self.path, live=True).first()
        if parent.is_chapter_page:
            # if there is no next page look for the next chapter
            if not next_page:
                next_page = parent.get_siblings().filter(path__gt=self.path, live=True).first()
                # if there is no next chapter return to the parent.get_parent()
                if not next_page:
                    next_page = parent.get_parent()
        else:
            # Parent is a PublicationPage, not a chapter page
            # if there is no next page, return the parent
            if not next_page:
                next_page = parent

        return next_page

    @property
    def prev_page(self):
        """
        Get the previous page for a publication. Details below:

        Check the parent page type. If the parent page type is a "Chapter Page",
        then look for siblings of `this` page. If no previous sibling can be found
        look for the parent page previous sibling. And if that cannot be found,
        return the Chapter Page's parent (Publication Page).
        Otherwise if the parent page is a Publication page: look for the previous sibling,
        if there is no previous sibling page, return this pages' parent.
        """

        parent = self.get_parent().specific
        prev_page = self.get_siblings().filter(path__lt=self.path, live=True).reverse().first()
        if parent.is_chapter_page:
            # look for the previous page in this chapter
            # if there is no previous page look for the previous chapter
            if not prev_page:
                prev_page = parent.get_siblings().filter(path__lt=self.path, live=True).reverse().first()
                # if there is no previous chapter return to the parent.get_parent()
                if not prev_page:
                    prev_page = parent.get_parent()
        else:
            # Parent is a PublicationPage, not a chapter page
            # look for the previous page in this publication
            # if there is no previous page, return the parent
            if not prev_page:
                prev_page = parent

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
        context['get_titles'] = get_plaintext_titles(request, self.body, "content")
        return set_main_site_nav_information(self, context, 'Homepage')
