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

# from networkapi.wagtailpages.pagemodels.libraries.rcc import authors_index
# from networkapi.wagtailpages.pagemodels.profiles import Profile
# from networkapi.wagtailpages.utils import localize_queryset

logger = logging.getLogger(__name__)


class RCCDetailPage(BasePage):
    # parent_page_types = ["RCCLibraryPage"]

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
        # edit_handlers.InlinePanel("research_links", heading="Research links"),
        edit_handlers.FieldPanel("original_publication_date"),
        edit_handlers.FieldPanel("introduction"),
        edit_handlers.FieldPanel("overview"),
        # edit_handlers.InlinePanel("research_authors", heading="Authors", min_num=1),
        edit_handlers.FieldPanel("contributors"),
        # edit_handlers.InlinePanel("related_topics", heading="Topics"),
        # edit_handlers.InlinePanel("related_regions", heading="Regions"),
    ]

    translatable_fields = [
        localize_fields.TranslatableField("title"),
        localize_fields.SynchronizedField("cover_image"),
        localize_fields.SynchronizedField("original_publication_date", overridable=False),
        # localize_fields.TranslatableField("research_links"),
        localize_fields.TranslatableField("introduction"),
        localize_fields.TranslatableField("overview"),
        # localize_fields.TranslatableField("research_authors"),
        # Contributors is translatable in case of connecting words like "and"
        localize_fields.TranslatableField("contributors"),
        # localize_fields.TranslatableField("related_topics"),
        # localize_fields.TranslatableField("related_regions"),
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
        # index.RelatedFields(
        #     "research_authors",
        #     [
        #         index.RelatedFields(
        #             "author_profile",
        #             [index.SearchField("name")],
        #         )
        #     ],
        # ),
        # index.RelatedFields(
        #     "related_topics",
        #     [
        #         index.RelatedFields(
        #             "research_topic",
        #             [index.SearchField("name")],
        #         )
        #     ],
        # ),
        # index.RelatedFields(
        #     "related_regions",
        #     [
        #         index.RelatedFields(
        #             "research_region",
        #             [index.SearchField("name")],
        #         )
        #     ],
        # ),
    ]

    # def get_context(self, request):
    #     context = super().get_context(request)
    #     # context["authors_index"] = authors_index.ResearchAuthorsIndexPage.objects.first()
    #     # context["research_authors"] = self.get_research_authors()
    #     return context

    # def get_authors(self):
    #     research_author_profiles = localize_queryset(
    #         Profile.objects.prefetch_related("authored_research").filter(authored_research__research_detail_page=self)
    #     )
    #     return research_author_profiles

    # def get_research_author_names(self):
    #     return [ra.author_profile.name for ra in self.research_authors.all()]

    # def get_related_topic_names(self):
    #     return [rt.research_topic.name for rt in self.related_topics.all()]

    def get_banner(self):
        return self.get_parent().specific.get_banner()
