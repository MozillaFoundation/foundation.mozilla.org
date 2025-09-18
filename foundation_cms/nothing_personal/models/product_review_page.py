from django.db import models
from django.utils.functional import cached_property
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, FieldRowPanel, MultiFieldPanel
from wagtail.models import Orderable
from wagtail_localize.fields import SynchronizedField, TranslatableField

from foundation_cms.base.models.abstract_article_page import AbstractArticlePage
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
    show_what_you_should_know_section = models.BooleanField(
        default=False, verbose_name="Show 'What You Should Know' Section"
    )
    show_reduce_your_risks_section = models.BooleanField(
        default=False, verbose_name="Show 'Reduce Your Risks' Section"
    )
    show_the_good_and_the_bad_section = models.BooleanField(
        default=False, verbose_name="Show 'The Good and The Bad' Section"
    )
    show_the_bottom_line_section = models.BooleanField(default=False, verbose_name="Show 'The Bottom Line' Section")

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
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("show_what_you_should_know_section"),
                        FieldPanel("show_reduce_your_risks_section"),
                    ]
                ),
                FieldRowPanel(
                    [
                        FieldPanel("show_the_good_and_the_bad_section"),
                        FieldPanel("show_the_bottom_line_section"),
                    ]
                ),
            ],
            heading="Product Review Sections",
            help_text="Choose which sections will appear in this product review",
        ),
        FieldPanel("lede_text"),
    ]

    parent_page_types = ["nothing_personal.NothingPersonalHomePage"]
    subpage_types: list[str] = []

    translatable_fields = [
        # Content tab fields
        SynchronizedField("show_what_you_should_know_section"),
        SynchronizedField("show_reduce_your_risks_section"),
        SynchronizedField("show_the_good_and_the_bad_section"),
        SynchronizedField("show_the_bottom_line_section"),
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
        return context

    def get_preview_context(self, request, mode_name):
        context = super().get_preview_context(request, mode_name)
        context["products_mentioned"] = self.preview_products_mentioned
        context["anchor_sections"] = self.get_anchor_sections()
        return context

    def get_anchor_sections(self):
        """Generate anchor sections based on enabled sections"""
        section_mapping = [
            (self.show_what_you_should_know_section, "What You Should Know", "what-you-should-know"),
            (self.show_reduce_your_risks_section, "Reduce Your Risks", "reduce-your-risks"),
            (self.show_the_good_and_the_bad_section, "The Good and The Bad", "the-good-and-the-bad"),
            (self.show_the_bottom_line_section, "The Bottom Line", "the-bottom-line"),
        ]

        return [{"title": title, "anchor": anchor} for enabled, title, anchor in section_mapping if enabled]

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
