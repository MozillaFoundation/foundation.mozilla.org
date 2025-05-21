from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField

from foundation_cms.base.models.abstract_base_page import AbstractBasePage
from foundation_cms.base.models.image_blocks import SingleImageBlock, DoubleImageBlock


class AbstractGeneralPage(AbstractBasePage):
    sized_images = StreamField(
        [
            ("single_image", SingleImageBlock(label="Single Image")),
            ("double_image", DoubleImageBlock(label="Double Image")),
        ],
        use_json_field=True,
        blank=True,
        help_text="Add images with different layout options",
    )

    content_panels = AbstractBasePage.content_panels + [
        FieldPanel("sized_images"),
    ]

    class Meta:
        abstract = True
