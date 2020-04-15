from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel

from networkapi.buyersguide.fields import ExtendedYesNoField
from .base import BaseProduct, register_product_type


class SoftwareProduct(BaseProduct):
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

    signup_with_contact_info = models.BooleanField(
        null=True,
        help_text='Email or phone number required to sign up? Email/Phone = Yes, Third Party Acount = No',
    )

    signup_with_contact_info_helptext = models.TextField(
        max_length=5000,
        blank=True
    )

    medical_privacy_compliant = models.BooleanField(
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

    # TODO: make these fit in the right place
    panels = BaseProduct.panels + [
        MultiFieldPanel(
            [
                FieldPanel('handles_recordings_how'),
                FieldPanel('recording_alert'),
                FieldPanel('recording_alert_helptext'),
                FieldPanel('signup_with_contact_info'),
                FieldPanel('signup_with_contact_info_helptext'),
                FieldPanel('medical_privacy_compliant'),
                FieldPanel('medical_privacy_compliant_helptext'),
            ],
            heading='how does it handle privacy?',
            classname='collapsible'
        ),
        MultiFieldPanel(
            [
                FieldPanel('host_controls'),
                FieldPanel('easy_to_learn_and_use'),
                FieldPanel('easy_to_learn_and_use_helptext'),
            ],
            heading='can I control it',
            classname='collapsible'
        ),
    ]

    # todict function
    def to_dict(self):
        model_dict = super().to_dict()
        model_dict['product_type'] = 'software'
        return model_dict


# Register this model class so that BaseProduct can "cast" properly
register_product_type(SoftwareProduct)
