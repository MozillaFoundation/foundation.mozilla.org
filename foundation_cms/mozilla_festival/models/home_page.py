from wagtail.admin.panels import FieldPanel
from wagtail_localize.fields import TranslatableField

from foundation_cms.base.models.abstract_home_page import AbstractHomePage


class MozfestHomePage(AbstractHomePage):
    max_count = 1

    content_panels = AbstractHomePage.content_panels + [
        FieldPanel("body"),
    ]

    translatable_fields = AbstractHomePage.translatable_fields + [
        # Content tab fields
        TranslatableField("body"),
    ]

    template = "patterns/pages/mozilla_festival/home_page.html"

    class Meta:
        verbose_name = "Mozfest Home Page"

    def get_context(self, request):
        context = super().get_context(request)
        return context
