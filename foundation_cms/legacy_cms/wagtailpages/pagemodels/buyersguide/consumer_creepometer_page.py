from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.models import Locale
from wagtail_localize.fields import SynchronizedField

from foundation_cms.legacy_cms.wagtailpages.pagemodels.base import BasePage
from foundation_cms.legacy_cms.wagtailpages.pagemodels.buyersguide.forms import (
    BuyersGuideArticlePageForm,
)
from foundation_cms.legacy_cms.wagtailpages.pagemodels.buyersguide.homepage import (
    BuyersGuidePage,
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
        bg_page = self.get_parent().get_parent().specific
        context["methodology_url"] = bg_page.url + bg_page.reverse_subpage("methodology-view")
        return context
