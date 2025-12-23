from wagtail.admin.panels import FieldPanel
from wagtail.search import index
from wagtail_localize.fields import TranslatableField

from foundation_cms.base.models.abstract_article_page import AbstractArticlePage
from foundation_cms.nothing_personal.models.product_review_page import (
    NothingPersonalProductReviewPage,
)
from foundation_cms.utils import get_default_locale, localize_queryset


class NothingPersonalProductCollectionPage(AbstractArticlePage):

    content_panels = AbstractArticlePage.content_panels + [
        FieldPanel("lede_text"),
    ]

    translatable_fields = AbstractArticlePage.translatable_fields + [
        # Content tab fields
        TranslatableField("body"),
        TranslatableField("lede_text"),
    ]

    search_fields = AbstractArticlePage.search_fields + [
        index.SearchField("lede_text", boost=5),
        index.SearchField("body", boost=4),
    ]

    parent_page_types = ["nothing_personal.NothingPersonalHomePage"]
    subpage_types: list[str] = []

    class Meta:
        verbose_name = "Nothing Personal Product Collection Page"

    template = "patterns/pages/nothing_personal/product_collection_page.html"

    def get_context(self, request):
        context = super().get_context(request)
        (default_locale, _) = get_default_locale()
        product_reviews = (
            NothingPersonalProductReviewPage.objects.live()
            .public()
            .filter(locale=default_locale)
            .order_by("-first_published_at")
        )
        localized_reviews = localize_queryset(product_reviews, preserve_order=True)
        context["product_reviews"] = localized_reviews.specific()

        return context
