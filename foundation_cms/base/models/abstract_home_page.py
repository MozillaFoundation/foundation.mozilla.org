from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField

from foundation_cms.base.models.abstract_base_page import AbstractBasePage


class AbstractHomePage(AbstractBasePage):
    body = StreamField(
        [
            # Placeholder for homepage-specific layout blocks
        ],
        use_json_field=True,
        blank=True,
    )

    content_panels = AbstractBasePage.content_panels + [FieldPanel("body")]

    class Meta:
        abstract = True
