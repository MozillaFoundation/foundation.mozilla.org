from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail_localize.fields import TranslatableField

from foundation_cms.base.models.abstract_general_page import AbstractGeneralPage


class GeneralPage(AbstractGeneralPage):
    # Specify the correct template path
    template = "patterns/pages/core/general_page.html"

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
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Hero Image",
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

    content_panels = AbstractGeneralPage.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("show_hero"),
                FieldPanel("hero_variant"),
                FieldPanel("hero_title"),
                FieldPanel("hero_description"),
                FieldPanel("hero_image"),
            ],
            heading="Hero Section",
            classname="collapsible",
        ),
        FieldPanel("button_title"),
        FieldPanel("button_url"),
    ]

    translatable_fields = [
        TranslatableField("hero_title"),
        TranslatableField("hero_description"),
        TranslatableField("button_title"),
    ]

    class Meta:
        verbose_name = "General Page (new)"

    def get_context(self, request):
        context = super().get_context(request)
        return context
