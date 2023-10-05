from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail_localize.fields import SynchronizedField
from wagtail.models import Locale

from networkapi.wagtailpages.pagemodels.base import BasePage
from networkapi.wagtailpages.pagemodels.buyersguide.homepage import BuyersGuidePage
from networkapi.wagtailpages.pagemodels.buyersguide.forms import (
    BuyersGuideArticlePageForm,
)


class ConsumerCreepometerPage(BasePage):
    parent_page_types = ["wagtailpages.BuyersGuideEditorialContentIndexPage"]
    subpage_types: list = []
    template = "buyersguide/pages/consumer_creepometer_page.html"
    # Custom base form for additional validation
    base_form_class = BuyersGuideArticlePageForm

    YEAR_CHOICES = (("2023", "2023"),)

    year = models.CharField(
        choices=YEAR_CHOICES, default="2023", help_text="Which year is this page for?", max_length=4
    )

    content_panels = BasePage.content_panels + [
        FieldPanel("year"),
    ]

    translatable_fields = [
        SynchronizedField("year"),
    ]

    @property
    def bg_page(self):
        active_locale = Locale.get_active()
        return BuyersGuidePage.objects.get(locale=active_locale)

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["methodology_url"] = self.bg_page.url + self.bg_page.reverse_subpage("methodology-view")
        return context
