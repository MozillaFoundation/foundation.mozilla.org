from django.db import models
from modelcluster.fields import ParentalKey

from wagtail.core.models import Orderable, Page
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, StreamFieldPanel
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from wagtail_localize.fields import SynchronizedField, TranslatableField

from networkapi.wagtailpages.models import ContentAuthor, PublicationPage
from networkapi.wagtailpages.utils import get_plaintext_titles, set_main_site_nav_information, TitleWidget

from ..mixin.foundation_metadata import FoundationMetadataPageMixin
from ..article_fields import article_fields


class ArticleAuthors(Orderable):
    """This allows us to select one or more blog authors from Snippets."""

    page = ParentalKey("wagtailpages.ArticlePage", related_name="authors")

    author = models.ForeignKey(
        ContentAuthor,
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

    Articles can belong to any page in the Wagtail Tree.
    An ArticlePage can have no children
    If not a child of a Publication Page, page nav at bottom of page
    and breadcrumbs will not render.
    """
    subpage_types = []
    body = StreamField(article_fields)

    toc_thumbnail_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Table of Content Thumbnail',
        help_text='Thumbnail image to show on table of content. Use square image of 320×320 pixels or larger.',
    )

    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
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

    article_file = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    show_side_share_buttons = models.BooleanField(
        default=True,
        help_text="Show social share buttons on the side"
    )

    content_panels = [
        FieldPanel(
            "title",
            classname="full title",
            widget=TitleWidget(attrs={"class": "max-length-warning", "data-max-length": 60})
        ),
        MultiFieldPanel([
            InlinePanel("authors", label="Author", min_num=0)
        ], heading="Author(s)"),
        MultiFieldPanel([
            ImageChooserPanel("toc_thumbnail_image"),
        ], heading="Table of Content Thumbnail"),
        MultiFieldPanel([
            ImageChooserPanel("hero_image"),
            FieldPanel('subtitle'),
            FieldPanel('secondary_subtitle'),
            FieldPanel('publication_date'),
            DocumentChooserPanel('article_file'),
        ], heading="Hero"),
        FieldPanel('show_side_share_buttons'),
        StreamFieldPanel('body'),
        InlinePanel("footnotes", label="Footnotes"),
    ]

    translatable_fields = [
        # Promote tab fields
        SynchronizedField('slug'),
        TranslatableField('seo_title'),
        SynchronizedField('show_in_menus'),
        TranslatableField('search_description'),
        SynchronizedField('search_image'),
        # Content tab fields
        TranslatableField('title'),
        SynchronizedField('toc_thumbnail_image'),
        SynchronizedField('hero_image'),
        TranslatableField('subtitle'),
        SynchronizedField('article_file'),
        TranslatableField('body'),
        TranslatableField('footnotes'),
    ]

    @property
    def is_publication_article(self):
        parent = self.get_parent().specific
        return parent.__class__ is PublicationPage

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
