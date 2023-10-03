from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail_localize.fields import SynchronizedField

from networkapi.wagtailpages.pagemodels.base import BasePage
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


