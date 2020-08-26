
from django.db import models
from django.db.models import QuerySet
from typing import Union

from modelcluster.fields import ParentalKey

from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Orderable, Page
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from ..mixin.foundation_metadata import FoundationMetadataPageMixin
from networkapi.wagtailpages.models import BlogAuthor


class PublicationAuthors(Orderable):
    """This allows us to select one or more blog authors from Snippets."""

    page = ParentalKey("wagtailpages.PublicationPage", related_name="authors")
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
        return f"Author: {self.author.name}"


class PublicationPage(FoundationMetadataPageMixin, Page):
    """
    This is the root page of a publication.

    From here the user can browse to the various sections (called chapters).
    It will have information on the publication, its authors, and metadata from it's children

    Publications are collections of Articles
    Publications can also be broken down into Chapters, which are really just child publication pages
    Each of those Chapters may have several Articles
    An Article can only belong to one Chapter/Publication Page
    """

    subpage_types = ['ArticlePage', 'PublicationPage']

    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='publication_hero_image',
        verbose_name='Publication Hero Image',
    )
    subtitle = models.CharField(
        blank=True,
        max_length=250,
    )
    secondary_subtitle = models.CharField(
        blank=True,
        max_length=250,
    )
    publication_date = models.DateField(
        "Publication date",
        null=True,
        blank=True
    )
    publication_file = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    additional_author_copy = models.CharField(
        help_text="Example: with contributing authors",
        max_length=100,
        blank=True,
    )
    notes = RichTextField(
        blank=True,
    )
    contents_title = models.CharField(
        blank=True,
        default="Table of Contents",
        max_length=250,
    )
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('subtitle'),
            FieldPanel('secondary_subtitle'),
            FieldPanel('publication_date'),
            ImageChooserPanel('hero_image'),
            DocumentChooserPanel('publication_file'),
            InlinePanel("authors", label="Author"),
            FieldPanel("additional_author_copy"),
        ], heading="Hero"),
        FieldPanel('contents_title'),
        FieldPanel('notes')
    ]

    @property
    def is_chapter_page(self) -> bool:
        """Is this a chapter page (child-Publicationpage). Returns a bool."""
        parent = self.get_parent().specific
        return parent.__class__.__name__ == self.__class__.__name__

    @property
    def my_children(self):
        """
        See: https://django-treebeard.readthedocs.io/en/stable/api.html#treebeard.models.Node.get_annotated_list
        This works almost perfectly for us except design spec has us exclude the parent
        from the list, hence the pop()
        """

        children_summary = self.get_annotated_list(parent=self)
        children_summary.pop(0)
        return children_summary

    def get_chapter_number_or_none(self) -> Union[int, None]:
        """Return the chapter page number or None."""
        if self.is_chapter_page:
            chapter_pages = list(self.get_siblings().specific())
            return chapter_pages.index(self) + 1
        return None

    def get_child_article_pages(self) -> Union[QuerySet, list]:
        """
        Returns all the live Article pages under this page type.

        If this is a ChapterPage (second level or deeper PublicationPage) return
        a QuerySet of child pages. Otherwise return none.
        """
        return self.get_children().type(ArticlePage).live() if self.is_chapter_page else []

    def get_child_chapter_pages(self) -> Union[QuerySet, list]:
        """
        If the page is a first-level PublicationPage (not a Chapter Page), get child chapters.
        """
        return self.get_children().type(PublicationPage).live() if not self.is_chapter_page else []
