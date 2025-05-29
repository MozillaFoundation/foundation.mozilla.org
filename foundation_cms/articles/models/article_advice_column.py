from foundation_cms.base.models.abstract_article_page import AbstractArticlePage


class ArticleAdviceColumn(AbstractArticlePage):

    content_panels = AbstractArticlePage.content_panels + [
        # Placeholder for ArticleAdviceColumn blocks
    ]

    parent_page_types = ["core.HomePage"]
    subpage_types: list[str] = []

    class Meta:
        verbose_name = "Article Advice Column"

    template = "patterns/pages/articles/article_advice_column.html"

    def get_context(self, request):
        context = super().get_context(request)
        return context
