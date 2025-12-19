from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField

from foundation_cms.base.models.abstract_base_page import (
    BASE_BLOCK_NAMES,
    AbstractBasePage,
)
from foundation_cms.blocks.block_registry import BlockRegistry

# General page-specific blocks that extend the base blocks
GENERAL_PAGE_BLOCK_NAMES = sorted(
    BASE_BLOCK_NAMES
    + [
        "custom_media",
    ]
)
general_page_block_options = BlockRegistry.get_blocks(GENERAL_PAGE_BLOCK_NAMES)


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
