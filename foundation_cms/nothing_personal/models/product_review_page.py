from django.db import models
from django.utils.functional import cached_property
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Orderable
from wagtail_localize.fields import SynchronizedField, TranslatableField

from foundation_cms.base.models.abstract_article_page import AbstractArticlePage
from foundation_cms.blocks import (
    ProductReviewSectionBottomLineBlock,
    ProductReviewSectionGoodAndBadBlock,
    ProductReviewSectionReduceYourRisksBlock,
    ProductReviewSectionWhatYouShouldKnowBlock,
)
from foundation_cms.blocks.newsletter_signup_block import NewsletterSignupBlock
from foundation_cms.constants import DEFAULT_RICH_TEXT_FEATURES
from foundation_cms.mixins.hero_image import HeroImageMixin
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
        verbose_name="Product",
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
    hours_tested = models.CharField(
        max_length=255, null=True, blank=True, help_text="Number of hours tested (e.g. '20')"
    )
    type_of_testing = models.CharField(max_length=255, null=True, blank=True, help_text="Type of testing")
    byline = models.CharField(max_length=100, null=True, blank=True, help_text="Byline")
    who_am_i = RichTextField(blank=True, help_text="Who am I? (rich text)", features=DEFAULT_RICH_TEXT_FEATURES)
    scoring = models.CharField(max_length=255, null=True, blank=True, help_text="Plain text field for product scoring")

    what_you_should_know_section = StreamField(
        [("content", ProductReviewSectionWhatYouShouldKnowBlock())],
        max_num=1,
        use_json_field=True,
        blank=True,
    )

    newsletter_signup_section = StreamField(
        [("content", NewsletterSignupBlock())],
        max_num=1,
        use_json_field=True,
        blank=True,
    )

    good_and_bad_section = StreamField(
        [("content", ProductReviewSectionGoodAndBadBlock())],
        max_num=1,
        use_json_field=True,
        blank=True,
    )

    reduce_your_risks_section = StreamField(
        [("content", ProductReviewSectionReduceYourRisksBlock())],
        max_num=1,
        use_json_field=True,
        blank=True,
    )

    bottom_line_section = StreamField(
        [("content", ProductReviewSectionBottomLineBlock())],
        max_num=1,
        use_json_field=True,
        blank=True,
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
                FieldPanel("hours_tested"),
                FieldPanel("type_of_testing"),
                FieldPanel("byline"),
                FieldPanel("who_am_i"),
                FieldPanel("scoring"),
            ],
            heading="Product Review Meta",
        ),
        FieldPanel("lede_text"),
        MultiFieldPanel(
            [
                FieldPanel("what_you_should_know_section"),
                FieldPanel("newsletter_signup_section"),
                FieldPanel("good_and_bad_section"),
                FieldPanel("reduce_your_risks_section"),
                FieldPanel("bottom_line_section"),
            ],
            heading="Review Sections",
        ),
        MultiFieldPanel(
            [InlinePanel("products_mentioned", max_num=4)],
            heading="Products Mentioned",
        ),
    ]

    parent_page_types = ["nothing_personal.NothingPersonalHomePage"]
    subpage_types: list[str] = []

    translatable_fields = AbstractArticlePage.translatable_fields + [
        # Content tab fields
        TranslatableField("what_you_should_know_section"),
        SynchronizedField("newsletter_signup_section"),
        TranslatableField("good_and_bad_section"),
        TranslatableField("reduce_your_risks_section"),
        TranslatableField("bottom_line_section"),
        SynchronizedField("products_mentioned"),
        SynchronizedField("hero_image"),
        TranslatableField("hero_image_alt_text"),
        SynchronizedField("updated"),
        SynchronizedField("reviewed"),
        TranslatableField("scoring"),
        TranslatableField("hours_tested"),
        TranslatableField("type_of_testing"),
        TranslatableField("byline"),
        TranslatableField("who_am_i"),
        TranslatableField("lede_text"),
    ]

    class Meta:
        verbose_name = "Nothing Personal Product Review"

    template = "patterns/pages/nothing_personal/product_review_page.html"

    def get_context(self, request):
        context = super().get_context(request)
        context["products_mentioned"] = self.localized_products_mentioned
        context["latest_product_reviews"] = self.get_latest_product_reviews()
        context["anchor_sections"] = self.get_anchor_sections()
        return context

    def get_preview_context(self, request, mode_name):
        context = super().get_preview_context(request, mode_name)
        context["products_mentioned"] = self.preview_products_mentioned
        context["anchor_sections"] = self.get_anchor_sections()
        return context

    def get_latest_product_reviews(self):
        """
        Returns the 5 latest `NothingPersonalProductReviewPage` objects.
        Uses current locale if available, falls back to default locale.
        """
        from wagtail.models import Locale

        current_locale = self.locale
        default_locale = Locale.get_default()

        default_reviews = (
            NothingPersonalProductReviewPage.objects.live()
            .public()
            .filter(locale=default_locale)
            .exclude(id=self.id)
            .order_by("-first_published_at")[:5]
        )

        # Get the best available version for each review
        localized_results = []
        for review in default_reviews:
            best_version = review.get_translation(locale=current_locale)
            if best_version and best_version.live:
                localized_results.append(best_version)

        return localized_results

    def get_anchor_sections(self):
        """Generate anchor sections based on individual page fields"""
        section_configs = [
            (
                "what_you_should_know",
                self.what_you_should_know_section,
                "What You Should Know",
                "what-you-should-know",
            ),
            ("good_and_bad", self.good_and_bad_section, "The Good and The Bad", "good-and-bad"),
            ("reduce_your_risks", self.reduce_your_risks_section, "Reduce Your Risks", "reduce-your-risks"),
            ("bottom_line", self.bottom_line_section, "The Bottom Line", "bottom-line"),
        ]

        sections = []
        for section_key, section_field, title, anchor in section_configs:
            if not section_field:
                continue

            sections.append({"title": title, "anchor": anchor})

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
        Fetches products mentioned updates for CMS page previews.
        """
        products_mentioned = get_related_items(
            self.products_mentioned.all(), "mentioned_product", order_by="sort_order"
        )

        return products_mentioned
