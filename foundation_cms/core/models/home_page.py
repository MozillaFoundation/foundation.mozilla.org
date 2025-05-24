from django.db import models
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel
from wagtail_localize.fields import TranslatableField

from foundation_cms.base.models.abstract_home_page import AbstractHomePage
from foundation_cms.blocks import HeroAccordionBlock

class HomePage(AbstractHomePage):
    hero_accordion = StreamField(
        HeroAccordionBlock(),
        min_num=2,
        max_num=3,
        verbose_name="Hero Accordion",
        blank=True,
    )

    content_panels = AbstractHomePage.content_panels + [
        FieldPanel("hero_accordion"),
        FieldPanel("body"),
    ]

    template = "patterns/pages/core/home_page.html"

    class Meta:
        verbose_name = "Home Page (new)"

    def get_context(self, request):
        context = super().get_context(request)
        return context
