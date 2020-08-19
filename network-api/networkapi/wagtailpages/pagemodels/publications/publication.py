
from django.db import models

from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.documents.models import Document
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.core.fields import RichTextField


from ..mixin.foundation_metadata import FoundationMetadataPageMixin


class PublicationPage(FoundationMetadataPageMixin, Page):
    """
    This is the root page of a publication. From here the user can browse to the various sections (called chapters).
    It will have information on the publication, its authors, and metadata from it's children
    """

    # TODO: once we make chapter pages, add that as a subpage type
    subpage_types = []

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

    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        FieldPanel('secondary_subtitle'),
        FieldPanel('publication_date'),
        ImageChooserPanel('hero_image'),
        DocumentChooserPanel('publication_file'),
        FieldPanel('contents_title')
    ]
