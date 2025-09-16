from django.db import models
from django.utils.functional import cached_property
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.models import Orderable
from wagtail_localize.fields import SynchronizedField

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
    ]

    parent_page_types = ["nothing_personal.NothingPersonalHomePage"]
    subpage_types: list[str] = []

    translatable_fields = [
        # Content tab fields
        SynchronizedField("products_mentioned"),
    ]

    class Meta:
        verbose_name = "Nothing Personal Product Review"

    template = "patterns/pages/nothing_personal/product_review_page.html"

    def get_context(self, request):
        context = super().get_context(request)
        context["products_mentioned"] = self.localized_products_mentioned
        return context

    def get_preview_context(self, request, mode_name):
        context = super().get_preview_context(request, mode_name)
        context["products_mentioned"] = self.preview_products_mentioned
        return context

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
