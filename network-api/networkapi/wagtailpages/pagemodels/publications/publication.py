
from django.db import models

from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.core.fields import RichTextField

from networkapi.wagtailpages.models import base_fields
from networkapi.wagtailpages.pagemodels.publications.article import ArticlePage

from ..mixin.foundation_metadata import FoundationMetadataPageMixin


class PublicationPage(FoundationMetadataPageMixin, Page):
    """
    This is the root page of a publication.

    From here the user can browse to the various sections (called chapters).
    It will have information on the publication, its authors, and metadata from it's children

    TODO: this poem is beautiful, but it may not belong here
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

    notes = RichTextField(
        blank=True,
    )

    contents_title = models.CharField(
        blank=True,
        default="Table of Contents",
        max_length=250,
    )

    # body = StreamField(base_fields)

    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        FieldPanel('secondary_subtitle'),
        FieldPanel('publication_date'),
        ImageChooserPanel('hero_image'),
        DocumentChooserPanel('publication_file'),
        FieldPanel('contents_title'),
        FieldPanel('notes')
    ]

    @property
    def is_chapter_page(self) -> bool:
        """Is this a chapter page (child-Publicationpage). Returns a bool."""
        parent = self.get_parent().specific
        return parent.__class__.__name__ == 'PublicationPage'

    def get_chapter_pages(self) -> list:
        pages = []
        if self.is_chapter_page:
            # Get all the chapter page siblings. Used for finding the number
            # of the Chapter. ie. Chapter 3.
            _chapters = list(self.get_siblings().specific())
            for _page in self.get_children().type(ArticlePage).live().specific():
                pages.append({
                    'page': _page,
                    'parent_chapter_number': _chapters.index(self) + 1,
                })
            return pages
        return pages
