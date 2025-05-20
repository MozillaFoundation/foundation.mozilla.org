from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail_localize.fields import TranslatableField

from foundation_cms.base.models.abstract_general_page import AbstractGeneralPage


class GeneralPage(AbstractGeneralPage):
    # Specify the correct template path
    template = "patterns/pages/core/general_page.html"
    
    hero_headline = models.CharField(
        max_length=120,
        help_text="Hero story headline",
        blank=True,
    )

    hero_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Hero Image",
    )

    header = models.TextField(
        blank=True,
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
        FieldPanel("hero_headline"),
        FieldPanel("hero_image"),
        FieldPanel("header"),
        FieldPanel("button_title"),
        FieldPanel("button_url"),
        FieldPanel("body"),
    ]

    translatable_fields = [
        TranslatableField("hero_headline"),
        TranslatableField("header"),
        TranslatableField("button_title"),
    ]

    class Meta:
        verbose_name = "General Page (new)"

    def get_context(self, request):
        context = super().get_context(request)
        return context
