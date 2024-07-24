from functools import cached_property

from django.db import models
from modelcluster import fields as cluster_fields
from wagtail.admin import panels as wagtail_panels
from wagtail.search import index
from wagtail_localize import fields as localize_fields

from networkapi.utility import orderables
from networkapi.wagtailpages import utils as wagtailpages_utils
from networkapi.wagtailpages.pagemodels import profiles
from networkapi.wagtailpages.pagemodels.libraries import detail_page as base_detail_page
from networkapi.wagtailpages.pagemodels.libraries.rcc import authors_index


class RCCDetailPage(base_detail_page.LibraryDetailPage):
    parent_page_types = ["RCCLibraryPage"]

    template = "pages/libraries/rcc/detail_page.html"

    content_panels = base_detail_page.LibraryDetailPage.content_panels + [
        wagtail_panels.MultipleChooserPanel(
            "related_content_types", heading="Content types", chooser_field_name="content_type"
        ),
        wagtail_panels.MultipleChooserPanel(
            "related_curricular_areas", heading="Curricular areas", chooser_field_name="curricular_area"
        ),
        wagtail_panels.MultipleChooserPanel("related_topics", heading="Topics", chooser_field_name="topic"),
    ]

    translatable_fields = base_detail_page.LibraryDetailPage.translatable_fields + [
        localize_fields.TranslatableField("related_content_types"),
        localize_fields.TranslatableField("related_curricular_areas"),
        localize_fields.TranslatableField("related_topics"),
    ]

    search_fields = base_detail_page.LibraryDetailPage.search_fields + [
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
                    "topic",
                    [index.SearchField("name")],
                )
            ],
        ),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context["content_type_names"] = self.related_content_types_names
        return context

    def get_preview_template(self, request, mode_name):
        return "previews/libraries/rcc/detail_page.html"

    @cached_property
    def localized_authors(self):
        rcc_author_profiles = profiles.Profile.objects.filter(authored_rcc_articles__detail_page=self).order_by(
            "authored_rcc_articles__sort_order"
        )
        rcc_author_profiles = wagtailpages_utils.localize_queryset(rcc_author_profiles, preserve_order=True)
        return rcc_author_profiles

    @property
    def preview_related_authors(self):
        """
        Fetches related authors for CMS page previews.
        """
        related_authors = orderables.get_related_items(self.authors.all(), "author_profile", order_by="sort_order")

        return related_authors

    @cached_property
    def authors_index_page(self):
        return authors_index.RCCAuthorsIndexPage.objects.first()

    @property
    def authors_detail_url_name(self):
        return "rcc-author-detail"

    @cached_property
    def related_content_types_names(self):
        return [ct.content_type.name for ct in self.related_content_types.all()]

    class Meta(base_detail_page.LibraryDetailPage.Meta):
        verbose_name = "RCC detail page"
        verbose_name_plural = "RCC detail pages"


class RCCDetailLink(base_detail_page.LibraryDetailLinkBase):
    detail_page = cluster_fields.ParentalKey(
        "RCCDetailPage",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="links",
    )
