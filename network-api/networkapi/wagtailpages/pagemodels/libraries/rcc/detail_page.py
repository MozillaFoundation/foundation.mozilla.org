from functools import cached_property

from django.db import models
from modelcluster import fields as cluster_fields
from wagtail.admin import panels as wagtail_panels
from wagtail.search import index
from wagtail_localize import fields as localize_fields

from networkapi.wagtailpages import utils as wagtailpages_utils
from networkapi.wagtailpages.pagemodels import profiles
from networkapi.wagtailpages.pagemodels.libraries import detail_page as base_detail_page
from networkapi.wagtailpages.pagemodels.libraries.rcc import authors_index


class RCCDetailPage(base_detail_page.LibraryDetailPage):
    parent_page_types = ["RCCLibraryPage"]

    template = "pages/libraries/rcc/detail_page.html"

    content_panels = base_detail_page.LibraryDetailPage.content_panels + [
        wagtail_panels.InlinePanel("related_content_types", heading="Content types"),
        wagtail_panels.InlinePanel("related_curricular_areas", heading="Curricular areas"),
        wagtail_panels.InlinePanel("related_topics", heading="Topics"),
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

    @cached_property
    def localized_authors(self):
        rcc_author_profiles = wagtailpages_utils.localize_queryset(
            profiles.Profile.objects.filter(authored_rcc_articles__detail_page=self)
        )
        return rcc_author_profiles

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
