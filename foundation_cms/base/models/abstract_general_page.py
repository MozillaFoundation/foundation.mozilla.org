from wagtail.admin.panels import FieldPanel

from foundation_cms.base.models.abstract_base_page import AbstractBasePage


class AbstractGeneralPage(AbstractBasePage):

    content_panels = AbstractBasePage.content_panels + [
        FieldPanel("body"),
    ]

    translatable_fields = AbstractBasePage.translatable_fields

    class Meta:
        abstract = True
