from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.images import get_image_model_string
from wagtail_localize.fields import TranslatableField

from foundation_cms.base.models.abstract_general_page import AbstractGeneralPage


class GeneralPage(AbstractGeneralPage):
    hero_title = models.TextField(
        help_text="Hero Title",
        blank=True,
    )

    hero_description = models.CharField(
        max_length=120,
        help_text="Hero Description",
        blank=True,
    )

    hero_media_type = models.CharField(
        max_length=20,
        choices=[
            ("image", "Image"),
            ("video", "Video"),
        ],
        default="image",
        verbose_name="Hero Media Type",
        help_text="Select the media type for Hero Section.",
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

    hero_video = models.ForeignKey(
        "wagtailmedia.Media",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Hero Video",
        help_text="Video for page hero section.",
    )

    hero_variant = models.CharField(
        max_length=50,
        choices=[
            ("side-by-side", "Side by Side"),
            ("top-to-bottom", "Top to Bottom"),
        ],
        default="side-by-side",
        help_text="Select the variant of the hero section",
    )

    hero_background_color = models.CharField(
        max_length=50,
        choices=[
            ("orange-200", "Orange"),
            ("yellow-200", "Yellow"),
        ],
        default="orange-200",
        help_text="Select the color of the hero background, only for 'Top to Bottom' variant.",
    )

    show_hero = models.BooleanField(
        default=True,
        verbose_name="Show Hero Section",
        help_text="Check to display the hero section on this page.",
    )

    button_title = models.CharField(
        verbose_name="Button Text",
        max_length=250,
        blank=True,
    )

    button_url = models.TextField(
        verbose_name="Button URL",
        blank=True,
    )

    content_panels = [
        FieldPanel("title"),
        MultiFieldPanel(
            [
                FieldPanel("show_hero"),
                FieldPanel("hero_variant"),
                FieldPanel("hero_background_color"),
                FieldPanel("hero_title"),
                FieldPanel("hero_description"),
                FieldPanel("hero_media_type"),
                MultiFieldPanel(
                    [
                        FieldPanel("hero_image"),
                        FieldPanel("hero_image_alt_text"),
                    ],
                    heading="Hero Image Settings",
                ),
                FieldPanel("hero_video"),
            ],
            heading="Hero Section",
            classname="collapsible",
        ),
        FieldPanel("button_title"),
        FieldPanel("button_url"),
        FieldPanel("body"),
    ]

    translatable_fields = [
        TranslatableField("hero_title"),
        TranslatableField("hero_description"),
        TranslatableField("button_title"),
        TranslatableField("hero_image_alt_text"),
    ]

    class Meta:
        verbose_name = "General Page (new)"

    # keep an explicit fallback in case no themed templates exist
    template = "patterns/pages/core/general_page.html"
