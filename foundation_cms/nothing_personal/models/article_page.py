from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.images import get_image_model_string

from foundation_cms.base.models.abstract_article_page import AbstractArticlePage
from foundation_cms.mixins.hero_image import HeroImageMixin
from foundation_cms.utils import get_default_locale


class NothingPersonalArticlePage(AbstractArticlePage, HeroImageMixin):

    displayed_hero_content = models.CharField(
        max_length=25,
        choices=[
            ("image", "Image"),
            ("video", "Video"),
            ("none", "None"),
        ],
        default="none",
        help_text="Choose what type of content appears in the hero section.",
    )

    hero_video = models.CharField(
        blank=True,
        max_length=500,
        help_text="Log into Vimeo using 1Password "
        "and upload the desired video. "
        "Then select the video and "
        'click "Advanced", "Distribution", '
        'and "Video File Links". Copy and paste the link here.',
    )

    content_panels = AbstractArticlePage.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("displayed_hero_content"),
                FieldPanel("hero_image"),
                FieldPanel("hero_image_alt_text"),
                FieldPanel("hero_video"),
            ],
            heading="Hero Section",
            classname="collapsible",
        ),
        FieldPanel("lede_text"),
        FieldPanel("body"),
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
