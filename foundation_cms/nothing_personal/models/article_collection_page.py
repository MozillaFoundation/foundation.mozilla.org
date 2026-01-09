from wagtail.admin.panels import FieldPanel
from wagtail.search import index
from wagtail_localize.fields import TranslatableField

from foundation_cms.base.models.abstract_article_page import AbstractArticlePage
from foundation_cms.nothing_personal.models.article_page import (
    NothingPersonalArticlePage,
)
from foundation_cms.utils import get_default_locale, localize_queryset


class NothingPersonalArticleCollectionPage(AbstractArticlePage):

    content_panels = AbstractArticlePage.content_panels + [
        FieldPanel("lede_text"),
    ]

    translatable_fields = AbstractArticlePage.translatable_fields + [
        # Content tab fields
        TranslatableField("body"),
        TranslatableField("lede_text"),
    ]

    search_fields = AbstractArticlePage.search_fields + [
        index.SearchField("lede_text", boost=6),
        index.SearchField("body", boost=4),
    ]

    parent_page_types = ["nothing_personal.NothingPersonalHomePage"]
    subpage_types: list[str] = []

    class Meta:
        verbose_name = "Nothing Personal Article Collection Page"

    template = "patterns/pages/nothing_personal/article_collection_page.html"

    def get_context(self, request):
        context = super().get_context(request)
        (DEFAULT_LOCALE, _) = get_default_locale()
        article_pages = (
            NothingPersonalArticlePage.objects.live()
            .public()
            .filter(locale=DEFAULT_LOCALE)
            .order_by("-first_published_at")
        )
        localized_article_pages = localize_queryset(article_pages, preserve_order=True)
        context["localized_article_pages"] = localized_article_pages.specific()
        context["article_page_results_count"] = localized_article_pages.count()
        return context
