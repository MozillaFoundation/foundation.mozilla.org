from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail_localize.fields import TranslatableField

from foundation_cms.base.models.abstract_home_page import AbstractHomePage

hero_intro_heading_default_text = "A healthy internet is one in which privacy, openness, and inclusion are the norms."
hero_intro_body_default_text = (
    "Mozilla empowers consumers to demand better online privacy, trustworthy AI, "
    "and safe online experiences from Big Tech and governments. We work across "
    "borders, disciplines, and technologies to uphold principles like privacy, "
    "inclusion and decentralization online."
)


class HomePage(AbstractHomePage):
    content_panels = AbstractHomePage.content_panels + [
        FieldPanel("body"),
    ]

    translatable_fields = []

    template = "patterns/pages/core/home_page.html"

    class Meta:
        verbose_name = "Home Page (new)"

    def get_context(self, request):
        context = super().get_context(request)
        return context
