from wagtail.admin.panels import FieldPanel
from wagtail.search import index
from wagtail_localize.fields import SynchronizedField, TranslatableField

from foundation_cms.base.models.abstract_article_page import AbstractArticlePage
from foundation_cms.core.panels.media_panel import MediaPanel
from foundation_cms.mixins.hero_media import HeroMediaMixin

HERO_CONTENT_IMAGE = "image"
HERO_CONTENT_VIDEO = "video"


class NothingPersonalArticlePage(AbstractArticlePage, HeroMediaMixin):

    content_panels = AbstractArticlePage.content_panels + [
        MediaPanel.create_default(
            heading="Hero Section",
            classname="collapsible",
            trigger_field="displayed_hero_content",
            image_field="hero_image",
            video_field="hero_video_url",
        ),
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

    search_fields = AbstractArticlePage.search_fields + [
        index.SearchField("lede_text", boost=6),
        index.SearchField("hero_image_alt_text", boost=2),
    ]

    parent_page_types = ["nothing_personal.NothingPersonalHomePage"]
    subpage_types: list[str] = []

    class Meta:
        verbose_name = "Nothing Personal Article Page"

    template = "patterns/pages/nothing_personal/article_page.html"

    def get_latest_articles(self):
        """
        Returns the 2 latest `NothingPersonalArticlePage` objects.
        Uses current locale if available, falls back to default locale.
        """
        from wagtail.models import Locale

        current_locale = self.locale
        default_locale = Locale.get_default()

        default_articles = (
            NothingPersonalArticlePage.objects.live()
            .public()
            .filter(locale=default_locale)
            .exclude(id=self.id)
            .order_by("-first_published_at")[:2]
        )

        # Get the best available version for each article
        localized_results = []
        for article in default_articles:
            best_version = article.get_translation(locale=current_locale)
            if best_version and best_version.live:
                localized_results.append(best_version)

        return localized_results

    def get_context(self, request):
        context = super().get_context(request)
        context["latest_articles"] = self.get_latest_articles()
        return context
