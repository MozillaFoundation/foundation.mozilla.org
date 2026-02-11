from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail_localize.fields import SynchronizedField, TranslatableField

from foundation_cms.base.models.abstract_general_page import AbstractGeneralPage
from foundation_cms.core.panels.media_panel import MediaPanel
from foundation_cms.mixins.hero_image import HeroImageMixin


class GeneralPage(AbstractGeneralPage, HeroImageMixin):

    hero_description = models.CharField(
        max_length=120,
        help_text="Hero Description",
        blank=True,
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
        MediaPanel(
            [
                FieldPanel("show_hero"),
                FieldPanel("hero_variant"),
                FieldPanel(
                    "hero_background_color",
                    attrs={"data-media-target": "field", "data-condition": "top-to-bottom"},
                ),
                FieldPanel("hero_title"),
                FieldPanel("hero_description"),
                FieldPanel(
                    "hero_image",
                    help_text="Top to Bottom variant crops image to 16:9; Side by Side variant crops image to 1:1.",
                ),
                FieldPanel("hero_image_alt_text"),
            ],
            heading="Hero Section",
            classname="collapsible",
            trigger_field="hero_variant",
        ),
        FieldPanel("button_title"),
        FieldPanel("button_url"),
        FieldPanel("body"),
    ]

    translatable_fields = AbstractGeneralPage.translatable_fields + [
        # Content tab fields
        SynchronizedField("show_hero"),
        SynchronizedField("hero_variant"),
        SynchronizedField("hero_background_color"),
        TranslatableField("hero_title"),
        TranslatableField("hero_description"),
        SynchronizedField("hero_image"),
        TranslatableField("hero_image_alt_text"),
        TranslatableField("button_title"),
        TranslatableField("button_url"),
        TranslatableField("body"),
    ]

    class Meta:
        verbose_name = "General Page"

    # keep an explicit fallback in case no themed templates exist
    template = "patterns/pages/core/general_page.html"
