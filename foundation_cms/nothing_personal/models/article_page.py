from wagtail.admin.panels import FieldPanel
from wagtail_localize.fields import SynchronizedField, TranslatableField

from foundation_cms.base.models.abstract_article_page import AbstractArticlePage
from foundation_cms.core.panels.hero_media_panel import HeroMediaPanel
from foundation_cms.mixins.hero_media import HeroMediaMixin
from foundation_cms.utils import get_default_locale

HERO_CONTENT_IMAGE = "image"
HERO_CONTENT_VIDEO = "video"


class NothingPersonalArticlePage(AbstractArticlePage, HeroMediaMixin):

    content_panels = AbstractArticlePage.content_panels + [
        HeroMediaPanel.create_default(),
        FieldPanel("lede_text"),
        FieldPanel("body"),
    ]

    translatable_fields = AbstractArticlePage.translatable_fields + [
        # Content tab fields
        SynchronizedField("displayed_hero_content"),
        SynchronizedField("hero_image"),
        TranslatableField("hero_image_alt_text"),
        SynchronizedField("hero_video_url"),
        TranslatableField("lede_text"),
        TranslatableField("body"),
    ]

    parent_page_types = ["nothing_personal.NothingPersonalHomePage"]
    subpage_types: list[str] = []

    class Meta:
        verbose_name = "Nothing Personal Article Page"

    template = "patterns/pages/nothing_personal/article_page.html"

    def get_latest_articles(self):
        """
        Returns the 2 latest `NothingPersonalArticlePage` objects.
        """
        (DEFAULT_LOCALE, DEFAULT_LOCALE_ID) = get_default_locale()

        results = (
            NothingPersonalArticlePage.objects.live()
            .public()
            .filter(locale=DEFAULT_LOCALE)
            .exclude(id=self.id)
            .order_by("-first_published_at")[:2]
        )

        localized_results = [p.localized for p in results]

        return localized_results

    def get_context(self, request):
        context = super().get_context(request)
        context["latest_articles"] = self.get_latest_articles()
        return context
