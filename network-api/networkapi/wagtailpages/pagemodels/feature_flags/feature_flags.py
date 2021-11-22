from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, TabbedInterface, ObjectList
from wagtail.contrib.settings.models import BaseSetting, register_setting

@register_setting(icon='tick')
class FeatureFlags(BaseSetting):

    activate_donate_banner = models.BooleanField(
        default=False,
        verbose_name='Activate the donation banner',
        help_text='This will show our donation banner at the top of all foundation pages, when checked',
    )

    content_panels = [
        FieldPanel('activate_donate_banner')
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading="Feature Flags"),
    ])
