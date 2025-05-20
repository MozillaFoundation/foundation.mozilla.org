from wagtail.admin.panels import FieldPanel
from wagtail.blocks import RichTextBlock
from wagtail.fields import StreamField

from foundation_cms.base.models.abstract_base_page import AbstractBasePage
from foundation_cms.blocks.audio_block import AudioBlock


class AbstractArticlePage(AbstractBasePage):
    body = StreamField(
        [
            ("audio", AudioBlock()),
            ("rich_text", RichTextBlock()),
        ],
        use_json_field=True,
        blank=True,
    )

    content_panels = AbstractBasePage.content_panels + [
        FieldPanel("body"),
    ]

    class Meta:
        abstract = True
