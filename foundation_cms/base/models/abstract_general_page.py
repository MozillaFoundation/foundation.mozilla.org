from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField

from foundation_cms.base.models.abstract_base_page import (
    AbstractBasePage,
    base_page_block_options,
)
from foundation_cms.blocks import CustomMediaBlock

general_page_block_options = base_page_block_options + [
    ("custom_media", CustomMediaBlock()),
]


class AbstractGeneralPage(AbstractBasePage):

    body = StreamField(
        general_page_block_options,
        use_json_field=True,
        blank=True,
    )

    content_panels = AbstractBasePage.content_panels + [
        FieldPanel("body"),
    ]

    translatable_fields = AbstractBasePage.translatable_fields

    class Meta:
        abstract = True
