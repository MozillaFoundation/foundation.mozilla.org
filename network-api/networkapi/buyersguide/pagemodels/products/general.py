from django.db import models
from networkapi.buyersguide.fields import ExtendedYesNoField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel

from .base import BaseProduct
from ...utils import tri_to_quad


class GeneralProduct(BaseProduct):
    product_type = 'general'

    # It uses your...

    camera_device = ExtendedYesNoField(
        help_text='Does this device have or access a camera?',
    )

    camera_app = ExtendedYesNoField(
        help_text='Does the app have or access a camera?',
    )

    microphone_device = ExtendedYesNoField(
        help_text='Does this Device have or access a microphone?',
    )

    microphone_app = ExtendedYesNoField(
        help_text='Does this app have or access a microphone?',
    )

    location_device = ExtendedYesNoField(
        help_text='Does this product access your location?',
    )

    location_app = ExtendedYesNoField(
        help_text='Does this app access your location?',
    )

    # how it handles privacy

    delete_data = models.BooleanField(  # TO BE REMOVED?
        null=True,
        help_text='Can you request data be deleted?',
    )

    delete_data_helptext = models.TextField(  # TO BE REMOVED?
        max_length=5000,
        blank=True
    )

    parental_controls = ExtendedYesNoField(
        null=True,
        help_text='Are there rules for children?',
    )

    child_rules_helptext = models.TextField(  # TO BE REMOVED?
        max_length=5000,
        blank=True
    )

    collects_biometrics = ExtendedYesNoField(
        help_text='Does this product collect biometric data?',
    )

    collects_biometrics_helptext = models.TextField(
        max_length=5000,
        blank=True
    )

    # administrative panels

    # TODO: make these fit in the right place
    panels = BaseProduct.panels + [
        MultiFieldPanel(
            [
                FieldPanel('camera_device'),
                FieldPanel('camera_app'),
                FieldPanel('microphone_device'),
                FieldPanel('microphone_app'),
                FieldPanel('location_device'),
                FieldPanel('location_app'),
            ],
            heading='Can it snoop?',
            classname='collapsible'
        ),
        MultiFieldPanel(
            [
                FieldPanel('delete_data'),
                FieldPanel('delete_data_helptext'),
                FieldPanel('parental_controls'),
                FieldPanel('collects_biometrics'),
                FieldPanel('collects_biometrics_helptext'),
                FieldPanel('user_friendly_privacy_policy'),
                FieldPanel('user_friendly_privacy_policy_helptext'),
            ],
            heading='How does it handle privacy (general products)',
            classname='collapsible'
        ),
    ]

    # todict function
    def to_dict(self):
        model_dict = super.to_dict()
        model_dict['delete_data'] = tri_to_quad(self.delete_data)
        return model_dict
