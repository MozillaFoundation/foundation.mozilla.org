from django.db import models
from wagtail.admin.panels import FieldPanel

from foundation_cms.base.models.abstract_article_page import AbstractArticlePage


class ArticleProductReview(AbstractArticlePage):

    content_panels = AbstractArticlePage.content_panels + [
        # Placeholder for ArticleAdviceColumn blocks
    ]

    parent_page_types = ['core.HomePage']
    subpage_types: list[str] = []

    class Meta:
        verbose_name = "Article Product Review"

    def get_context(self, request):
        context = super().get_context(request)
        return context
