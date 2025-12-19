from django.db import models
from wagtail.fields import StreamField

from foundation_cms.base.models.abstract_base_page import (
    BASE_BLOCK_NAMES,
    AbstractBasePage,
)
from foundation_cms.blocks.block_registry import BlockRegistry

# Article page-specific blocks that extend the base blocks
ARTICLE_BLOCK_NAMES = sorted(
    BASE_BLOCK_NAMES
    + [
        "callout",
        "custom_media",
    ]
)
article_page_block_options = BlockRegistry.get_blocks(ARTICLE_BLOCK_NAMES)


class AbstractArticlePage(AbstractBasePage):

    lede_text = models.TextField(blank=True, help_text="Optional introductory lede text (plain text only).")

    body = StreamField(
        article_page_block_options,
        use_json_field=True,
        blank=True,
    )

    content_panels = AbstractBasePage.content_panels + [
        # Universal Article content panels will go here
    ]

    translatable_fields = AbstractBasePage.translatable_fields

    class Meta:
        abstract = True
