from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.images import get_image_model_string
from wagtail.search import index
from wagtail_localize.fields import SynchronizedField, TranslatableField

from foundation_cms.base.models.abstract_base_page import AbstractBasePage


class NothingPersonalPodcastPage(AbstractBasePage):
    hero_title = models.TextField(
        help_text="Hero Title",
        blank=True,
    )

    hero_description = models.CharField(
        max_length=120,
        help_text="Brief description of the hero (max 120 characters)",
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

    translatable_fields = AbstractBasePage.translatable_fields + [
        # Content tab fields
        TranslatableField("hero_title"),
        TranslatableField("hero_description"),
        SynchronizedField("hero_image"),
        TranslatableField("hero_image_alt_text"),
        TranslatableField("body"),
    ]

    search_fields = AbstractBasePage.search_fields + [
        index.SearchField("hero_title", boost=8),
        index.SearchField("hero_description", boost=6),
        index.SearchField("hero_image_alt_text", boost=2),
    ]

    parent_page_types = ["nothing_personal.NothingPersonalHomePage"]
    subpage_types: list[str] = []

    class Meta:
        verbose_name = "Nothing Personal Podcast Page"

    template = "patterns/pages/nothing_personal/podcast_page.html"
