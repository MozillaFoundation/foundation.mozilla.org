from django.core.exceptions import ValidationError
from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.images import get_image_model_string

from foundation_cms.base.models.abstract_article_page import AbstractArticlePage
from foundation_cms.mixins.hero_image import HeroImageMixin
from foundation_cms.utils import get_default_locale

HERO_CONTENT_IMAGE = "image"
HERO_CONTENT_VIDEO = "video"
HERO_CONTENT_NONE = "none"


class NothingPersonalArticlePage(AbstractArticlePage, HeroImageMixin):

    displayed_hero_content = models.CharField(
        max_length=25,
        choices=[
            (HERO_CONTENT_IMAGE, "Image"),
            (HERO_CONTENT_VIDEO, "Video"),
            (HERO_CONTENT_NONE, "None"),
        ],
        default=HERO_CONTENT_IMAGE,
        help_text="Choose what type of content appears in the hero section.",
    )

    hero_video_url = models.CharField(
        blank=True,
        max_length=500,
        help_text="Log into Vimeo using 1Password "
        "and upload the desired video. "
        "Then select the video and "
        'click "...", "Video File Links", '
        'and select "(mp4, 1920 x 1080)". Copy and paste the link here.',
    )

    content_panels = AbstractArticlePage.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("displayed_hero_content"),
                FieldPanel("hero_image"),
                FieldPanel("hero_image_alt_text"),
                FieldPanel("hero_video_url"),
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

    def clean(self):
        super().clean()
        errors = {}

        if self.displayed_hero_content == HERO_CONTENT_IMAGE and not self.hero_image:
            errors["hero_image"] = "Image was chosen as displayed hero content, but no image is set."

        if self.displayed_hero_content == HERO_CONTENT_VIDEO and not self.hero_video_url:
            errors["hero_video_url"] = "Video was chosen as displayed hero content, but no URL is set."

        if errors:
            raise ValidationError(errors)

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
