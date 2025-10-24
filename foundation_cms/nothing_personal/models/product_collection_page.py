from wagtail.admin.panels import FieldPanel
from wagtail_localize.fields import TranslatableField

from foundation_cms.base.models.abstract_article_page import AbstractArticlePage
from foundation_cms.nothing_personal.models.product_review_page import (
    NothingPersonalProductReviewPage,
)
from foundation_cms.utils import get_default_locale, localize_queryset


class ProductReviewCard:
    """Simple object to mimic a block with product_review property"""

    def __init__(self, product_review):
        self.product_review = product_review


class NothingPersonalProductCollectionPage(AbstractArticlePage):

    content_panels = AbstractArticlePage.content_panels + [
        FieldPanel("lede_text"),
    ]

    translatable_fields = AbstractArticlePage.translatable_fields + [
        # Content tab fields
        TranslatableField("body"),
        TranslatableField("lede_text"),
    ]

    parent_page_types = ["nothing_personal.NothingPersonalHomePage"]
    subpage_types: list[str] = []

    class Meta:
        verbose_name = "Nothing Personal Product Collection Page"

    template = "patterns/pages/nothing_personal/product_collection_page.html"

    def get_context(self, request):
        context = super().get_context(request)
        (DEFAULT_LOCALE, _) = get_default_locale()
        product_reviews = (
            NothingPersonalProductReviewPage.objects.live()
            .public()
            .filter(locale=DEFAULT_LOCALE)
            .order_by("-first_published_at")
        )
        localized_reviews = localize_queryset(product_reviews, preserve_order=True)
        context["product_reviews"] = localized_reviews.specific()

        # Create cards array with product_review property for template compatibility
        context["cards"] = [ProductReviewCard(review) for review in localized_reviews.specific()]

        return context
