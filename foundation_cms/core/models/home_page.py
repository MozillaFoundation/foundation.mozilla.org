from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail_localize.fields import TranslatableField

from foundation_cms.base.models.abstract_home_page import AbstractHomePage

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
