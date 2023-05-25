import logging

from django.core import exceptions
from django.db import models
from modelcluster import fields as cluster_fields
from wagtail import documents as wagtail_docs
from wagtail import fields as wagtail_fields
from wagtail import images as wagtail_images
from wagtail import models as wagtail_models
from wagtail.admin import panels as edit_handlers
from wagtail.images import edit_handlers as image_handlers
from wagtail.search import index
from wagtail_localize import fields as localize_fields

from networkapi.wagtailpages.pagemodels.base import BasePage
from networkapi.wagtailpages.pagemodels.customblocks.base_rich_text_options import (
    base_rich_text_options,
)
from networkapi.wagtailpages.pagemodels.libraries.rcc import authors_index
from networkapi.wagtailpages.pagemodels.profiles import Profile
from networkapi.wagtailpages.utils import localize_queryset

logger = logging.getLogger(__name__)


class RCCDetailPage(BasePage):
    parent_page_types = ["RCCLibraryPage"]

    subpage_types = ["ArticlePage", "PublicationPage"]

    template = "pages/rcc/detail_page.html"

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
            "Provide a short blurb about the article " "that will be displayed on listing pages and search results."
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
    contributors = models.TextField(
        null=False,
        blank=True,
        help_text="List all contributors that are not the project leading authors.",
    )

    content_panels = wagtail_models.Page.content_panels + [
        image_handlers.FieldPanel("cover_image"),
        edit_handlers.InlinePanel("rcc_links", heading="Article links"),
        edit_handlers.FieldPanel("original_publication_date"),
        edit_handlers.FieldPanel("introduction"),
        edit_handlers.FieldPanel("overview"),
        edit_handlers.InlinePanel("rcc_authors", heading="Authors", min_num=1),
        edit_handlers.FieldPanel("contributors"),
        edit_handlers.InlinePanel("related_content_types", heading="Content types"),
        edit_handlers.InlinePanel("related_curricular_areas", heading="Curricular areas"),
        edit_handlers.InlinePanel("related_topics", heading="Topics"),
    ]

    translatable_fields = [
        localize_fields.TranslatableField("title"),
        localize_fields.SynchronizedField("cover_image"),
        localize_fields.SynchronizedField("original_publication_date", overridable=False),
        localize_fields.TranslatableField("rcc_links"),
        localize_fields.TranslatableField("introduction"),
        localize_fields.TranslatableField("overview"),
        localize_fields.TranslatableField("rcc_authors"),
        # Contributors is translatable in case of connecting words like "and"
        localize_fields.TranslatableField("contributors"),
        localize_fields.TranslatableField("related_content_types"),
        localize_fields.TranslatableField("related_curricular_areas"),
        localize_fields.TranslatableField("related_topics"),
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
        index.SearchField("contributors"),
        index.FilterField("original_publication_date"),  # For sorting
        index.RelatedFields(
            "rcc_authors",
            [
                index.RelatedFields(
                    "author_profile",
                    [index.SearchField("name")],
                )
            ],
        ),
        index.RelatedFields(
            "related_content_types",
            [
                index.RelatedFields(
                    "content_type",
                    [index.SearchField("name")],
                )
            ],
        ),
        index.RelatedFields(
            "related_curricular_areas",
            [
                index.RelatedFields(
                    "curricular_area",
                    [index.SearchField("name")],
                )
            ],
        ),
        index.RelatedFields(
            "related_topics",
            [
                index.RelatedFields(
                    "rcc_topic",
                    [index.SearchField("name")],
                )
            ],
        ),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context["authors_index"] = authors_index.RCCAuthorsIndexPage.objects.first()
        context["rcc_authors"] = self.get_rcc_authors()
        context["rcc_author_names"] = self.get_rcc_author_names()
        context["content_type_names"] = self.get_related_content_types_names()
        return context

    def get_rcc_authors(self):
        rcc_author_profiles = localize_queryset(
            Profile.objects.prefetch_related("authored_rcc_entries").filter(authored_rcc_entries__rcc_detail_page=self)
        )
        return rcc_author_profiles

    def get_rcc_author_names(self):
        return [ra.author_profile.name for ra in self.rcc_authors.all()]

    def get_related_content_types_names(self):
        return [ct.content_type.name for ct in self.related_content_types.all()]

    def get_banner(self):
        return self.get_parent().specific.get_banner()


class RCCDetailLink(wagtail_models.TranslatableMixin, wagtail_models.Orderable):
    rcc_detail_page = cluster_fields.ParentalKey(
        "RCCDetailPage",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="rcc_links",
    )

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
        edit_handlers.HelpPanel(
            content=(
                "Please provide a link to the original resource. "
                "You can link to an internal page, an external URL or upload a document. "
                'If you wish to provide multiple, please create two separate "article links"'
            )
        ),
        edit_handlers.FieldPanel("label"),
        edit_handlers.FieldPanel("url"),
        edit_handlers.FieldPanel("page"),
        edit_handlers.FieldPanel("document"),
    ]

    class Meta(wagtail_models.TranslatableMixin.Meta, wagtail_models.Orderable.Meta):
        ordering = ["sort_order"]

    def __str__(self) -> str:
        return self.label

    def clean(self) -> None:
        super().clean()

        # Ensure that only one of the three fields is set
        if sum([bool(self.url), bool(self.page), bool(self.document)]) > 1:
            error_message = "Please provide either a URL, a page or a document, not multiple."
            raise exceptions.ValidationError(
                {"url": error_message, "page": error_message, "document": error_message},
                code="invalid",
            )
        # Ensure that at least one of the three fields is set
        elif not any([self.url, self.page, self.document]):
            error_message = "Please provide a URL, a page or a document."
            raise exceptions.ValidationError(
                {"url": error_message, "page": error_message, "document": error_message},
                code="required",
            )

    def get_url(self) -> str:
        if self.url:
            return self.url
        elif self.page:
            if not self.page.live:
                logger.warning(
                    f"Detail link to unpublished page defined: { self } -> { self.page }. "
                    "This link will not be shown in the frontend."
                )
                return ""
            return self.page.get_url()
        elif self.document:
            return self.document.url
        raise ValueError("No URL defined for this detail link. This should not happen.")
