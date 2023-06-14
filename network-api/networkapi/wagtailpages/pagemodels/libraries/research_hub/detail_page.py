import logging
from functools import cached_property

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

from networkapi.wagtailpages import utils as wagtailpages_utils
from networkapi.wagtailpages.pagemodels import profiles
from networkapi.wagtailpages.pagemodels.base import BasePage
from networkapi.wagtailpages.pagemodels.customblocks.base_rich_text_options import (
    base_rich_text_options,
)
from networkapi.wagtailpages.pagemodels.libraries import detail_page as base_detail_page
from networkapi.wagtailpages.pagemodels.libraries.research_hub import authors_index

logger = logging.getLogger(__name__)


class ResearchDetailPage(base_detail_page.LibraryDetailPage):
    parent_page_types = ["ResearchLibraryPage"]

    template = "pages/libraries/research_hub/detail_page.html"

    content_panels = base_detail_page.LibraryDetailPage.content_panels + [
        edit_handlers.InlinePanel("related_topics", heading="Topics"),
        edit_handlers.InlinePanel("related_regions", heading="Regions"),
    ]

    translatable_fields = base_detail_page.LibraryDetailPage.translatable_fields + [
        localize_fields.TranslatableField("related_topics"),
        localize_fields.TranslatableField("related_regions"),
    ]

    search_fields = base_detail_page.LibraryDetailPage.search_fields + [
        index.RelatedFields(
            "related_topics",
            [
                index.RelatedFields(
                    "topic",
                    [index.SearchField("name")],
                )
            ],
        ),
        index.RelatedFields(
            "related_regions",
            [
                index.RelatedFields(
                    "region",
                    [index.SearchField("name")],
                )
            ],
        ),
    ]

    @cached_property
    def localized_authors(self):
        research_author_profiles = wagtailpages_utils.localize_queryset(
            profiles.Profile.objects.filter(authored_research__detail_page=self)
        )
        return research_author_profiles

    @cached_property
    def authors_index_page(self):
        return authors_index.ResearchAuthorsIndexPage.objects.first()

    @property
    def authors_detail_url_name(self):
        return "research-author-detail"

    @cached_property
    def related_topic_names(self):
        return [rt.topic.name for rt in self.related_topics.all()]


class ResearchDetailLink(base_detail_page.LibraryDetailLinkBase):
    detail_page = cluster_fields.ParentalKey(
        "ResearchDetailPage",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="links",
    )
