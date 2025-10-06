from wagtail.admin.panels import FieldPanel

from foundation_cms.base.models.abstract_article_page import AbstractArticlePage
from foundation_cms.nothing_personal.models.product_review_page import (
    NothingPersonalProductReviewPage,
)
from foundation_cms.utils import get_default_locale, localize_queryset


class NothingPersonalArticleCollectionPage(AbstractArticlePage):

    content_panels = AbstractArticlePage.content_panels + [
        FieldPanel("lede_text"),
    ]

    parent_page_types = ["nothing_personal.NothingPersonalHomePage"]
    subpage_types: list[str] = []

    class Meta:
        verbose_name = "Nothing Personal Article Collection Page"

    template = "patterns/pages/nothing_personal/article_collection_page.html"

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
        return context
