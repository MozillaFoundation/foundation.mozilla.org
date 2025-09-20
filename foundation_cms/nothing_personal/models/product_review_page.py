from django.db import models
from django.utils.functional import cached_property
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import StreamField
from wagtail.models import Orderable
from wagtail_localize.fields import SynchronizedField, TranslatableField

from foundation_cms.base.models.abstract_article_page import AbstractArticlePage
from foundation_cms.blocks.newsletter_signup_block import NewsletterSignupBlock
from foundation_cms.mixins.hero_image import HeroImageMixin
from foundation_cms.nothing_personal.blocks import (
    BottomLineBlock,
    GoodAndBadBlock,
    ReduceYourRisksBlock,
    WhatYouShouldKnowBlock,
)
from foundation_cms.utils import get_related_items, localize_queryset


class ProductMentioned(Orderable):

    page = ParentalKey(
        "nothing_personal.NothingPersonalProductReviewPage",
        related_name="products_mentioned",
    )

    mentioned_product = models.ForeignKey(
        "nothing_personal.NothingPersonalProductReviewPage",
        on_delete=models.SET_NULL,
        null=True,
        related_name="mentioned_in_pages",
    )

    panels = [
        FieldPanel("mentioned_product"),
    ]

    def __str__(self):
        return self.mentioned_product.title

    class Meta(Orderable.Meta):
        verbose_name = "Product Mentioned"
        verbose_name_plural = "Products Mentioned"


class NothingPersonalProductReviewPage(AbstractArticlePage, HeroImageMixin):

    body = None
    updated = models.DateField(null=True, blank=True, help_text="When the review was last updated.")
    reviewed = models.DateField(null=True, blank=True, help_text="Date of the product review.")
    research = models.CharField(max_length=255, null=True, blank=True, help_text="Amount of time spent on research.")
    review_sections_block_options = [
        ("what_you_should_know", WhatYouShouldKnowBlock()),
        ("newsletter_signup", NewsletterSignupBlock()),
        ("reduce_your_risks", ReduceYourRisksBlock()),
        ("good_and_bad", GoodAndBadBlock()),
        ("bottom_line", BottomLineBlock()),
    ]

    review_sections = StreamField(
        review_sections_block_options,
        use_json_field=True,
        blank=True,
        block_counts={
            "what_you_should_know": {"max_num": 1},
            "newsletter_signup": {"max_num": 1},
            "reduce_your_risks": {"max_num": 1},
            "good_and_bad": {"max_num": 1},
            "bottom_line": {"max_num": 1},
        },
        max_num=5,
    )

    content_panels = AbstractArticlePage.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("hero_image"),
                FieldPanel("hero_image_alt_text"),
            ],
            heading="Hero Image",
        ),
        MultiFieldPanel(
            [
                FieldPanel("updated"),
                FieldPanel("reviewed"),
                FieldPanel("research"),
            ],
            heading="Product Review Meta",
        ),
        FieldPanel("lede_text"),
        MultiFieldPanel(
            [InlinePanel("products_mentioned", max_num=3)],
            heading="Products Mentioned",
        ),
        FieldPanel("review_sections"),
    ]

    parent_page_types = ["nothing_personal.NothingPersonalHomePage"]
    subpage_types: list[str] = []

    translatable_fields = [
        # Content tab fields
        SynchronizedField("review_sections"),
        SynchronizedField("products_mentioned"),
        SynchronizedField("hero_image"),
        TranslatableField("hero_image_alt_text"),
        SynchronizedField("updated"),
        SynchronizedField("reviewed"),
        TranslatableField("research"),
    ]

    class Meta:
        verbose_name = "Nothing Personal Product Review"

    template = "patterns/pages/nothing_personal/product_review_page.html"

    def get_context(self, request):
        context = super().get_context(request)
        context["products_mentioned"] = self.localized_products_mentioned
        context["anchor_sections"] = self.get_anchor_sections()
        context["ordered_review_sections"] = self.get_ordered_review_sections()
        return context

    def get_preview_context(self, request, mode_name):
        context = super().get_preview_context(request, mode_name)
        context["products_mentioned"] = self.preview_products_mentioned
        context["anchor_sections"] = self.get_anchor_sections()
        context["ordered_review_sections"] = self.get_ordered_review_sections()
        return context

    def get_ordered_review_sections(self):
        desired_order = [
            "what_you_should_know",
            "newsletter_signup",
            "reduce_your_risks",
            "good_and_bad",
            "bottom_line",
        ]

        blocks_by_type = {}
        for block in self.review_sections:
            blocks_by_type[block.block_type] = block

        has_what_you_should_know = "what_you_should_know" in blocks_by_type

        if not has_what_you_should_know and "newsletter_signup" in blocks_by_type:
            order_without_what_you_should_know = [
                "newsletter_signup",
                "reduce_your_risks",
                "good_and_bad",
                "bottom_line",
            ]
            desired_order = order_without_what_you_should_know

        ordered_blocks = []
        for block_type in desired_order:
            if block_type in blocks_by_type:
                if block_type == "bottom_line" and not self.products_mentioned.exists():
                    continue
                ordered_blocks.append(blocks_by_type[block_type])

        return ordered_blocks

    def get_anchor_sections(self):
        """Generate anchor sections based on review_sections StreamField"""
        sections = []

        section_mapping = {
            "what_you_should_know": {"title": "What You Should Know", "anchor": "what-you-should-know"},
            "reduce_your_risks": {"title": "Reduce Your Risks", "anchor": "reduce-your-risks"},
            "good_and_bad": {"title": "The Good and The Bad", "anchor": "good-and-bad"},
            "bottom_line": {"title": "The Bottom Line", "anchor": "bottom-line"},
        }

        for block in self.get_ordered_review_sections():
            if block.block_type in section_mapping:
                sections.append(section_mapping[block.block_type])

        return sections

    @cached_property
    def localized_products_mentioned(self):
        products_mentioned = NothingPersonalProductReviewPage.objects.filter(mentioned_in_pages__page=self).order_by(
            "mentioned_in_pages__sort_order"
        )
        localized_products_mentioned = localize_queryset(products_mentioned, preserve_order=True)

        return localized_products_mentioned.specific()

    @cached_property
    def preview_products_mentioned(self):
        """
        Fetches prodcts mentioned updates for CMS page previews.
        """
        products_mentioned = get_related_items(
            self.products_mentioned.all(), "mentioned_product", order_by="sort_order"
        )

        return products_mentioned
