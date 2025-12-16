from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    PageChooserPanel,
)
from wagtail.contrib.routable_page.models import RoutablePageMixin
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Orderable, Page
from wagtail.search import index
from wagtail_localize.fields import SynchronizedField, TranslatableField

from foundation_cms.base.models.abstract_home_page import AbstractHomePage
from foundation_cms.blocks import (
    ProductReviewCarouselBlock,
    TextMediaBlock,
    TwoColumnContainerBlock,
)


class NothingPersonalFeaturedItem(Orderable):
    """Orderable child model to allow 0..3 featured pages."""

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
        ("text_media_block", TextMediaBlock()),
        ("product_review_carousel_block", ProductReviewCarouselBlock(skip_default_wrapper=True)),
        # NP Text Image Block
        # product review carousel block
        # 50/50 block
    ]
    body = StreamField(
        nothing_personal_block_options,
        use_json_field=True,
        blank=True,
    )

    tagline = RichTextField(
        blank=True,
        features=["bold", "italic", "link"],
        help_text="Tagline displayed above the featured articles (max ~150 chars).",
    )

    hero_item = models.ForeignKey(
        Page,
        related_name="+",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    hero_item_orientation = models.CharField(
        max_length=20,
        choices=[
            ("square", "Square"),
            ("landscape", "Landscape"),
        ],
        default="square",
    )

    parent_page_types = ["core.HomePage"]
    subpage_types = [
        "nothing_personal.NothingPersonalArticleCollectionPage",
        "nothing_personal.NothingPersonalArticlePage",
        "nothing_personal.NothingPersonalPodcastPage",
        "nothing_personal.NothingPersonalProductCollectionPage",
        "nothing_personal.NothingPersonalProductReviewPage",
    ]

    content_panels = AbstractHomePage.content_panels + [
        FieldPanel("tagline"),
        MultiFieldPanel(
            [
                PageChooserPanel("hero_item"),
                FieldPanel("hero_item_orientation"),
            ],
            heading="Hero item",
        ),
        InlinePanel("featured_items", min_num=0, max_num=3, label="Featured items"),
        FieldPanel("body"),
    ]

    translatable_fields = AbstractHomePage.translatable_fields + [
        # Content tab fields
        TranslatableField("body"),
        TranslatableField("tagline"),
        SynchronizedField("hero_item"),
        SynchronizedField("hero_item_orientation"),
        SynchronizedField("featured_items"),
    ]

    search_fields = AbstractHomePage.search_fields + [
        index.SearchField("tagline", boost=6),
        index.SearchField("body", boost=7),
        index.RelatedFields(
            "hero_item",
            [
                index.SearchField("title", boost=4),
            ],
        ),
        index.RelatedFields(
            "featured_items",
            [
                index.SearchField("page__title", boost=3),
            ],
        ),
    ]

    class Meta:
        verbose_name = "Nothing Personal Home Page"

    template = "patterns/pages/nothing_personal/home_page.html"

    def get_context(self, request, virtual_page_name=None):
        context = super().get_context(request)

        if virtual_page_name:
            context["page_type_bem"] = self._to_bem_case(virtual_page_name)

        return context
