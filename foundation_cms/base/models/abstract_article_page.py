from django.db import models
from wagtail.fields import StreamField
from wagtail_localize.fields import TranslatableField

from foundation_cms.base.models.abstract_base_page import (
    AbstractBasePage,
    base_page_block_options,
)
from foundation_cms.blocks import CalloutBlock, CustomMediaBlock

# Article page-specific blocks that extend the base blocks
article_page_block_options = base_page_block_options + [
    ("callout", CalloutBlock()),
    ("custom_media", CustomMediaBlock()),
]


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

    class Meta:
        abstract = True
