from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel, PageChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin
from wagtail.fields import StreamField
from wagtail.models import Orderable, Page

from foundation_cms.base.models.abstract_home_page import AbstractHomePage
from foundation_cms.blocks import (
    NarrowTextImageBlock,
    ProductReviewCarouselBlock,
    TwoColumnContainerBlock,
)


class NothingPersonalFeaturedItem(Orderable):
    """Orderable child model to allow 0..4 featured pages."""

    page = models.ForeignKey(
        Page,
        related_name="+",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    home_page = ParentalKey(
        "nothing_personal.NothingPersonalHomePage",
        related_name="featured_items",
    )

    panels = [
        PageChooserPanel("page"),
    ]


class NothingPersonalHomePage(RoutablePageMixin, AbstractHomePage):

    max_count = 1

    nothing_personal_block_options = [
        ("two_column_container_block", TwoColumnContainerBlock()),
        ("narrow_text_image_block", NarrowTextImageBlock()),
        ("product_review_carousel_block", ProductReviewCarouselBlock()),
        # NP Text Image Block
        # product review carousel block
        # 50/50 block
    ]
    body = StreamField(
        nothing_personal_block_options,
        use_json_field=True,
        blank=True,
    )

    parent_page_types = ["core.HomePage"]
    subpage_types = [
        "nothing_personal.NothingPersonalArticleCollectionPage",
        "nothing_personal.NothingPersonalArticlePage",
        "nothing_personal.NothingPersonalPodcastPage",
        "nothing_personal.NothingPersonalProductReviewPage",
    ]

    content_panels = AbstractHomePage.content_panels + [
        InlinePanel("featured_items", min_num=0, max_num=4, label="Featured items"),
        FieldPanel("body"),
    ]

    class Meta:
        verbose_name = "Nothing Personal Home Page"

    template = "patterns/pages/nothing_personal/home_page.html"

    def get_context(self, request, virtual_page_name=None):
        context = super().get_context(request)

        if virtual_page_name:
            context["page_type_bem"] = self._to_bem_case(virtual_page_name)

        return context
