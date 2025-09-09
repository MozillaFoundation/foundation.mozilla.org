from wagtail.admin.panels import FieldPanel
from wagtail_localize.fields import TranslatableField

from foundation_cms.base.models.abstract_base_page import AbstractBasePage


class AbstractGeneralPage(AbstractBasePage):

    content_panels = AbstractBasePage.content_panels + [
        FieldPanel("body"),
    ]

    translatable_fields = AbstractBasePage.translatable_fields + [
        # Content tab fields
        TranslatableField("body"),
    ]

    class Meta:
        abstract = True
