from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.blocks import RichTextBlock


from foundation_cms.base.models.abstract_base_page import AbstractBasePage


class AbstractArticlePage(AbstractBasePage):
    body = StreamField(
        [
            # Placeholder for real blocks
            ("rich_text", RichTextBlock()),
        ],
        use_json_field=True,
        blank=True,
    )

    content_panels = AbstractBasePage.content_panels + [FieldPanel("body")]

    class Meta:
        abstract = True
