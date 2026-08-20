from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.search import index
from wagtail_localize.fields import SynchronizedField, TranslatableField

from foundation_cms.base.models.abstract_article_page import AbstractArticlePage
from foundation_cms.core.panels.media_panel import MediaPanel
from foundation_cms.mixins.hero_media import HeroMediaMixin

HERO_CONTENT_IMAGE = "image"
HERO_CONTENT_VIDEO = "video"


class NothingPersonalArticlePage(AbstractArticlePage, HeroMediaMixin):

    lede_text = models.TextField(blank=True, help_text="Optional introductory lede text (plain text only).")

    hero_caption = models.CharField(
        max_length=70,
        blank=True,
        verbose_name="Hero caption",
        help_text="Optional credit displayed beneath the hero image or video.",
    )

    share_section_heading = models.CharField(
        max_length=255,
        default="Enjoyed this? Share it!",
        help_text="Heading displayed above the SoSha share section.",
    )

    sosha_toolkit_embed_code = models.CharField(
        blank=True,
        verbose_name="SoSha Toolkit Embed Code",
        help_text=(
            "Optional SoSha toolkit embed code. When provided, the share"
            " section is rendered between the article body and topics."
        ),
    )

    content_panels = AbstractArticlePage.content_panels + [
        MediaPanel(
            [
                FieldPanel("displayed_hero_content"),
                FieldPanel(
                    "hero_image",
                    attrs={
                        "data-media-target": "field",
                        "data-condition": HeroMediaMixin.HERO_CONTENT_IMAGE,
                    },
                ),
                FieldPanel(
                    "hero_image_alt_text",
                    attrs={
                        "data-media-target": "field",
                        "data-condition": HeroMediaMixin.HERO_CONTENT_IMAGE,
                    },
                ),
                FieldPanel(
                    "hero_video_url",
                    attrs={
                        "data-media-target": "field",
                        "data-condition": HeroMediaMixin.HERO_CONTENT_VIDEO,
                    },
                ),
                FieldPanel("hero_caption"),
            ],
            heading="Hero Section",
            classname="collapsible",
            trigger_field="displayed_hero_content",
        ),
        FieldPanel("lede_text"),
        FieldPanel("body"),
        MultiFieldPanel(
            [
                FieldPanel("share_section_heading"),
                FieldPanel("sosha_toolkit_embed_code"),
            ],
            heading="Share Section",
            classname="collapsible",
        ),
    ]

    translatable_fields = AbstractArticlePage.translatable_fields + [
        # Content tab fields
        SynchronizedField("displayed_hero_content"),
        SynchronizedField("hero_image"),
        TranslatableField("hero_image_alt_text"),
        SynchronizedField("hero_video_url"),
        TranslatableField("hero_caption"),
        TranslatableField("lede_text"),
        TranslatableField("body"),
        TranslatableField("share_section_heading"),
        SynchronizedField("sosha_toolkit_embed_code"),
    ]

    search_fields = AbstractArticlePage.search_fields + [
        index.SearchField("lede_text", boost=8),
        index.SearchField("hero_image_alt_text", boost=2),
        index.SearchField("hero_caption", boost=2),
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
