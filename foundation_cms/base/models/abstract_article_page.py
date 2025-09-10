from django.db import models
from wagtail.admin.panels import FieldPanel

from foundation_cms.base.models.abstract_base_page import AbstractBasePage
from foundation_cms.mixins.lede_text import LedeTextMixin


class AbstractArticlePage(AbstractBasePage, LedeTextMixin):

    content_panels = AbstractBasePage.content_panels + [
        # Universal Article content panels ill go here
    ]

    class Meta:
        abstract = True
