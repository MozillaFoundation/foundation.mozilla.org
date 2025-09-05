from foundation_cms.base.models.abstract_article_page import AbstractArticlePage


class NothingPersonalProductReviewPage(AbstractArticlePage):

    content_panels = AbstractArticlePage.content_panels + [
        # Placeholder for NothingPersonalProductReviewPage blocks
    ]

    parent_page_types = ["nothing_personal.NothingPersonalHomePage"]
    subpage_types: list[str] = []

    class Meta:
        verbose_name = "Nothing Personal Product Review"

    template = "patterns/pages/nothing_personal/product_review_page.html"

    def get_context(self, request):
        context = super().get_context(request)
        return context
