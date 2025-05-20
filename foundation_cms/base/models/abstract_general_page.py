from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField

from foundation_cms.base.models.abstract_base_page import AbstractBasePage
from foundation_cms.base.models.image_blocks import SizedImageBlock


class AbstractGeneralPage(AbstractBasePage):
    sized_images = StreamField(
        [
            ("sized_image", SizedImageBlock()),
        ],
        use_json_field=True,
        blank=True,
        help_text="Images with size variations and titles",
    )

    content_panels = AbstractBasePage.content_panels + [
        FieldPanel("sized_images"),
    ]

    class Meta:
        abstract = True
