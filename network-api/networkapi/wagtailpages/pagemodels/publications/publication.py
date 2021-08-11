from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Orderable, Page
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from wagtail_localize.fields import SynchronizedField, TranslatableField

from networkapi.wagtailpages.models import ContentAuthor
from networkapi.wagtailpages.utils import set_main_site_nav_information
from ..mixin.foundation_metadata import FoundationMetadataPageMixin


class PublicationAuthors(Orderable):
    """This allows us to select one or more blog authors from Snippets."""

    page = ParentalKey("wagtailpages.PublicationPage", related_name="authors")

    author = models.ForeignKey(
        ContentAuthor, on_delete=models.SET_NULL, null=True, blank=False
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

    toc_thumbnail_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='toc_thumbnail_image',
        verbose_name='Table of Content Thumbnail',
        help_text='Thumbnail image to show on table of content. Use square image of 320×320 pixels or larger.',
    )

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
    publication_date = models.DateField("Publication date", null=True, blank=True)
    publication_file = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    additional_author_copy = models.CharField(
        help_text="Example: with contributing authors",
        max_length=100,
        blank=True,
    )
    intro_notes = RichTextField(
        blank=True,
        features=['link', 'bold', 'italic', 'h4']
    )
    notes = RichTextField(
        blank=True,
        features=['link', 'bold', 'italic', 'h4', 'ol', 'ul']
    )
    contents_title = models.CharField(
        blank=True,
        default="Table of Contents",
        max_length=250,
    )
    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel('subtitle'),
                FieldPanel('secondary_subtitle'),
                FieldPanel('publication_date'),
                ImageChooserPanel('toc_thumbnail_image'),
                ImageChooserPanel('hero_image'),
                DocumentChooserPanel('publication_file'),
                InlinePanel('authors', label='Author'),
                FieldPanel('additional_author_copy'),
            ],
            heading='Hero',
        ),
        FieldPanel('intro_notes'),
        FieldPanel('contents_title'),
        FieldPanel('notes'),
    ]

    translatable_fields = [
        # Promote tab fields
        SynchronizedField('slug'),
        TranslatableField('seo_title'),
        SynchronizedField('show_in_menus'),
        TranslatableField('search_description'),
        SynchronizedField('search_image'),
        # Content tab fields
        TranslatableField("title"),
        TranslatableField("subtitle"),
        TranslatableField('secondary_subtitle'),
        SynchronizedField('toc_thumbnail_image'),
        SynchronizedField('hero_image'),
        SynchronizedField('publication_date'),
        SynchronizedField('publication_file'),
        TranslatableField('additional_author_copy'),
        TranslatableField('intro_notes'),
        TranslatableField('contents_title'),
        TranslatableField('notes'),
    ]

    @property
    def is_publication_page(self):
        """
        Returning true to let publication_hero.html to show breadcrumbs
        """
        return True

    @property
    def is_chapter_page(self):
        """
        A PublicationPage nested under a PublicationPage is considered to be a
        "ChapterPage". The templates used very similar logic and structure, and
        all the fields are the same.
        """
        parent = self.get_parent().specific
        return parent.__class__ is PublicationPage

    @property
    def next_page(self):
        """
        Only applies to Chapter Publication (sub-Publication Pages).
        Returns a Page object or None.
        """
        next_page = self.get_parent()
        if self.is_chapter_page:
            sibling = self.get_siblings().filter(path__gt=self.path, live=True).first()
            if sibling:
                # If there is no more chapters. Return the parent page.
                next_page = sibling
        return next_page

    @property
    def prev_page(self):
        """
        Only applies to Chapter Publication (sub-Publication Pages).
        Returns a Page object or None.
        """
        prev_page = self.get_parent()
        if self.is_chapter_page:
            sibling = self.get_siblings().filter(path__lt=self.path, live=True).reverse().first()
            if sibling:
                # If there is no more chapters. Return the parent page.
                prev_page = sibling
        return prev_page

    @property
    def zen_nav(self):
        return True

    def breadcrumb_list(self):
        """
        Get all the parent PublicationPages and return a QuerySet
        """
        return Page.objects.ancestor_of(self).type(PublicationPage).live()

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        pages = []
        for page in self.get_children():
            if request.user.is_authenticated:
                # User is logged in, and can preview a page. Get all pages, even drafts.
                pages.append({
                    'child': page,
                    'grandchildren': page.get_children()
                })
            elif page.live:
                # User is not logged in AND this page is live. Only fetch live grandchild pages.
                pages.append({
                    'child': page,
                    'grandchildren': page.get_children().live()
                })
        context['child_pages'] = pages
        return set_main_site_nav_information(self, context, 'Homepage')
