from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.images import get_image_model_string

from foundation_cms.base.models.abstract_base_page import AbstractBasePage


class NothingPersonalPodcastPage(AbstractBasePage):
    hero_title = models.TextField(
        help_text="Hero Title",
        blank=True,
    )

    hero_description = models.CharField(
        max_length=120,
        help_text="Hero Description",
        blank=True,
    )

    hero_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Hero Image",
        help_text="Image for page hero section.",
    )

    hero_image_alt_text = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Alt Text",
        help_text="Descriptive text for screen readers. Leave blank to use the image's default title.",
    )

    content_panels = AbstractBasePage.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("hero_title"),
                FieldPanel("hero_description"),
                FieldPanel("hero_image"),
                FieldPanel("hero_image_alt_text"),
            ],
            heading="Hero Section",
            classname="collapsible",
        ),
        FieldPanel("body"),
    ]

    parent_page_types = ["nothing_personal.NothingPersonalHomePage"]
    subpage_types: list[str] = []

    class Meta:
        verbose_name = "Nothing Personal Podcast Page"

    template = "patterns/pages/nothing_personal/podcast_page.html"
