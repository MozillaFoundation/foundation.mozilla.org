from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel

from networkapi.buyersguide.fields import ExtendedYesNoField
from .base import Product, register_product_type

from networkapi.wagtailpages.utils import insert_panels_after


class SoftwareProduct(Product):
    """
    A thing you can install on your computer and our review of it
    """

    # How does it handle privacy?

    handles_recordings_how = models.TextField(
        max_length=5000,
        blank=True,
        help_text='How does this software handle your recordings'
    )

    recording_alert = ExtendedYesNoField(
        null=True,
        help_text='Alerts when calls are being recorded?',
    )

    recording_alert_helptext = models.TextField(
        max_length=5000,
        blank=True
    )

    medical_privacy_compliant = models.BooleanField(
        null=True,
        help_text='Compliant with US medical privacy laws?'
    )

    medical_privacy_compliant_helptext = models.TextField(
        max_length=5000,
        blank=True
    )

    # Can I control it?

    host_controls = models.TextField(
        max_length=5000,
        blank=True
    )

    easy_to_learn_and_use = models.BooleanField(
        null=True,
        help_text='Is it easy to learn & use the features?',
    )

    easy_to_learn_and_use_helptext = models.TextField(
        max_length=5000,
        blank=True
    )

    # administrative panels

    panels = Product.panels.copy()

    panels = insert_panels_after(
        panels,
        'General Product Details',
        [
            MultiFieldPanel(
                [
                    FieldPanel('handles_recordings_how'),
                    FieldPanel('recording_alert'),
                    FieldPanel('recording_alert_helptext'),
                    FieldPanel('medical_privacy_compliant'),
                    FieldPanel('medical_privacy_compliant_helptext'),
                ],
                heading='How does it handle privacy?',
                classname='collapsible'
            ),
            MultiFieldPanel(
                [
                    FieldPanel('host_controls'),
                    FieldPanel('easy_to_learn_and_use'),
                    FieldPanel('easy_to_learn_and_use_helptext'),
                ],
                heading='Can I control it',
                classname='collapsible'
            ),
        ],
    )

    def to_dict(self):
        model_dict = super().to_dict()
        model_dict['product_type'] = 'software'
        return model_dict


# Register this model class so that Product can "cast" properly
register_product_type(SoftwareProduct)
