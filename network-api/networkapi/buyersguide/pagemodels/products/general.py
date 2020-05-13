from django.db import models
from networkapi.buyersguide.fields import ExtendedYesNoField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel

from .base import Product, register_product_type
from ...utils import tri_to_quad

from networkapi.wagtailpages.utils import insert_panels_after


class GeneralProduct(Product):
    """
    A thing you can buy in stores and our review of it
    """

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

    panels = Product.panels.copy()

    panels = insert_panels_after(
        panels,
        'Minimum Security Standards for general products',
        [
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
        ],
    )

    panels = insert_panels_after(
        panels,
        'How does it handle data sharing',
        [
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
                heading='How does it handle privacy',
                classname='collapsible'
            ),
        ],
    )

    def to_dict(self):
        model_dict = super().to_dict()
        model_dict['delete_data'] = tri_to_quad(self.delete_data)
        model_dict['product_type'] = 'general'
        return model_dict


# Register this model class so that Product can "cast" properly
register_product_type(GeneralProduct)
