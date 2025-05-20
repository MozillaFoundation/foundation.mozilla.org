from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField

from foundation_cms.base.models.abstract_base_page import AbstractBasePage


class AbstractGeneralPage(AbstractBasePage):
    class Meta:
        abstract = True
