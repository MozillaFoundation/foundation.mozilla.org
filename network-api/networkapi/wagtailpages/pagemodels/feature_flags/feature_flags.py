from django.db import models
from wagtail.admin.panels import FieldPanel, ObjectList, TabbedInterface
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting


@register_setting(icon="tick")
class FeatureFlags(BaseSiteSetting):

    activate_donate_banner = models.BooleanField(
        default=False,
        verbose_name="Activate the donation banner",
        help_text="This will show our donation banner at the top of all foundation pages, when checked",
    )

    content_panels = [FieldPanel("activate_donate_banner")]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Feature Flags"),
        ]
    )
