from foundation_cms.base.models.abstract_article_page import AbstractArticlePage
from wagtail.admin.panels import FieldPanel


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
        return context
