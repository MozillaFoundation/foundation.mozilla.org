from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField, StreamField

from foundation_cms.base.models.abstract_base_page import AbstractBasePage


class AbstractArticlePage(AbstractBasePage):
    body = StreamField(
        [
            # Placeholder for real blocks
            ("rich_text", RichTextField()),
        ],
        use_json_field=True,
        blank=True,
    )

    content_panels = AbstractBasePage.content_panels + [
        FieldPanel("body"),
        FieldPanel("tags", classname="collapse"),
        ]

    class Meta:
        abstract = True
