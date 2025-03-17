import logging
from functools import cached_property

from django.core import exceptions
from django.db import models
from wagtail import documents as wagtail_docs
from wagtail import fields as wagtail_fields
from wagtail import images as wagtail_images
from wagtail import models as wagtail_models
from wagtail.admin import panels as wagtail_panels
from wagtail.search import index
from wagtail_localize import fields as localize_fields

from foundation_cms.legacy_apps.wagtailpages.pagemodels.base import BasePage
from foundation_cms.legacy_apps.wagtailpages.pagemodels.customblocks.base_rich_text_options import (
    base_rich_text_options,
)

logger = logging.getLogger(__name__)


class LibraryDetailPage(BasePage):
    """An abstract template for a library detail page.

    To define a concrete detail page, subclass it and implement the following properties:

    - `localized_authors`: Return the authors of this article in the current language.
    - `authors_index_page`: Return the authors index page.
    - `authors_detail_url_name`: Return the name of the URL pattern for the authors detail page.

    Authors need to be defined as a many2many relation to the `Profile` model.

    Taxonomies can also be included as many2many relations.

    Links to the original publication can be added as relationships to the
    `LibraryDetailLinkBase` model.

    Concrete implementation examples can be found in the RCC and Research_Hub apps.
    """

    subpage_types = ["ArticlePage", "PublicationPage"]

    cover_image = models.ForeignKey(
        wagtail_images.get_image_model_string(),
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        help_text=(
            "Select a cover image for this article. "
            "The cover image is displayed on the detail page and all article listings."
        ),
    )
    original_publication_date = models.DateField(
        null=True,
        blank=True,
        help_text="When was the article (not this page) originally published?",
    )
    introduction = models.CharField(
        null=False,
        blank=True,
        max_length=300,
        help_text=(
            "Provide a short blurb about the article that will be displayed on listing pages and search results."
        ),
    )
    overview = wagtail_fields.RichTextField(
        null=False,
        blank=True,
        features=base_rich_text_options,
        help_text=(
            "Provide an overview about the article. "
            "This can be an excerpt from or the executive summary of the original paper."
        ),
    )
    collaborators = models.TextField(
        null=False,
        blank=True,
        help_text="List all contributors that are not the project leading authors.",
    )

    content_panels = wagtail_models.Page.content_panels + [
        wagtail_panels.FieldPanel("cover_image"),
        wagtail_panels.InlinePanel("links", heading="Article links"),
        wagtail_panels.FieldPanel("original_publication_date"),
        wagtail_panels.FieldPanel("introduction"),
        wagtail_panels.FieldPanel("overview"),
        wagtail_panels.InlinePanel("authors", heading="Authors", min_num=1),
        wagtail_panels.FieldPanel("collaborators"),
    ]

    translatable_fields = [
        localize_fields.TranslatableField("title"),
        localize_fields.SynchronizedField("cover_image"),
        localize_fields.SynchronizedField("original_publication_date", overridable=False),
        localize_fields.TranslatableField("links"),
        localize_fields.TranslatableField("introduction"),
        localize_fields.TranslatableField("overview"),
        localize_fields.TranslatableField("authors"),
        # Promote tab fields
        localize_fields.SynchronizedField("slug"),
        localize_fields.TranslatableField("seo_title"),
        localize_fields.SynchronizedField("show_in_menus"),
        localize_fields.TranslatableField("search_description"),
        localize_fields.SynchronizedField("search_image"),
    ]

    search_fields = wagtail_models.Page.search_fields + [
        index.SearchField("introduction"),
        index.SearchField("overview"),
        index.SearchField("collaborators"),
        index.FilterField("original_publication_date"),  # For sorting
        index.RelatedFields(
            "authors",
            [
                index.RelatedFields(
                    "author_profile",
                    [index.SearchField("name")],
                )
            ],
        ),
    ]

    @property
    def localized_authors(self):
        """Return the authors of this article in the current language."""
        raise NotImplementedError("Please implement this property in your subclass.")

    @property
    def authors_index_page(self):
        """Return the authors index page."""
        raise NotImplementedError("Please implement this property in your subclass.")

    @property
    def authors_detail_url_name(self):
        """Return the name of the URL pattern for the authors detail page."""
        raise NotImplementedError("Please implement this property in your subclass.")

    @cached_property
    def author_names(self):
        """Return the names of the authors of this article."""
        return [author.name for author in self.localized_authors]

    def get_banner(self):
        return self.get_parent().specific.get_banner()

    class Meta:
        abstract = True


class LibraryDetailLinkBase(wagtail_models.TranslatableMixin, wagtail_models.Orderable):
    """An abstract template for a link to the original publication.

    To define a concrete detail link, subclass it and define a ParentalKey to the
    concrete detail page model.

    Concrete implementation examples can be found in the RCC and Research_Hub apps.
    """

    label = models.CharField(null=False, blank=False, max_length=50)

    url = models.URLField(null=False, blank=True)
    page = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    document = models.ForeignKey(
        wagtail_docs.get_document_model_string(),
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    panels = [
        wagtail_panels.HelpPanel(
            content=(
                "Please provide a link to the original resource. "
                "You can link to an internal page, an external URL or upload a document. "
                'If you wish to provide multiple, please create two separate "links"'
            )
        ),
        wagtail_panels.FieldPanel("label"),
        wagtail_panels.FieldPanel("url"),
        wagtail_panels.FieldPanel("page"),
        wagtail_panels.FieldPanel("document"),
    ]

    class Meta(wagtail_models.TranslatableMixin.Meta, wagtail_models.Orderable.Meta):
        abstract = True

    def __str__(self) -> str:
        return self.label

    def clean(self) -> None:
        super().clean()

        is_url_set = bool(self.url)
        is_page_set = bool(self.page)
        is_document_set = bool(self.document)

        # Ensure that only one of the three fields is set
        if sum([is_url_set, is_page_set, is_document_set]) > 1:
            error_message = "Please provide either a URL, a page or a document, not multiple."
            raise exceptions.ValidationError(
                {"url": error_message, "page": error_message, "document": error_message},
                code="invalid",
            )
        # Ensure that at least one of the three fields is set
        if not any([is_url_set, is_page_set, is_document_set]):
            error_message = "Please provide a URL, a page or a document."
            raise exceptions.ValidationError(
                {"url": error_message, "page": error_message, "document": error_message},
                code="required",
            )

    def get_url(self) -> str:
        if self.url:
            return self.url
        if self.page:
            if not self.page.live:
                logger.warning(
                    f"Detail link to unpublished page defined: { self } -> { self.page }. "
                    "This link will not be shown in the frontend."
                )
                return ""
            return self.page.localized.get_url()
        if self.document:
            return self.document.url
        raise ValueError("No URL defined for this detail link. This should not happen.")
