from foundation_cms.base.models.abstract_article_page import AbstractArticlePage


class NothingPersonalArticleCollectionPage(AbstractArticlePage):

    content_panels = AbstractArticlePage.content_panels + [
        # Placeholder for NothingPersonalArticleCollectionPage blocks
    ]

    parent_page_types = ["core.HomePage"]
    subpage_types: list[str] = []

    class Meta:
        verbose_name = "Nothing Personal Article Collection Page"

    template = "patterns/pages/nothing_personal/article_collection_page.html"

    def get_context(self, request):
        context = super().get_context(request)
        return context
