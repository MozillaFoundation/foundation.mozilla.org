from django.db import models
from networkapi.buyersguide.fields import ExtendedYesNoField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel

from .base import Product, register_product_type

from networkapi.wagtailpages.utils import insert_panels_after


class GeneralProduct(Product):
    """
    A thing you can buy in stores and our review of it
    """

    # Can it snoop on me

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

    # What data does it collect?

    personal_data_collected = models.TextField(
        max_length=5000,
        blank=True,
        help_text='What kind of personal data does this product collect?'
    )

    biometric_data_collected = models.TextField(
        max_length=5000,
        blank=True,
        help_text='What kind of biometric data does this product collect?'
    )

    social_data_collected = models.TextField(
        max_length=5000,
        blank=True,
        help_text='What kind of social data does this product collect?'
    )

    # How can you control your data

    how_can_you_control_your_data = models.TextField(
        max_length=5000,
        blank=True,
        help_text='How does this product let you control your data?'
    )

    data_control_policy_is_bad = models.BooleanField(
        default=False,
        verbose_name='Privacy ding'
    )

    # Company track record

    track_record_choices = [
        ('Great', 'Great'),
        ('Average', 'Average'),
        ('Needs Improvement', 'Needs Improvement'),
        ('Bad', 'Bad')
    ]

    company_track_record = models.CharField(
        choices=track_record_choices,
        default='Average',
        help_text='This company has a ... track record',
        max_length=20
    )

    track_record_is_bad = models.BooleanField(
        default=False,
        verbose_name='Privacy ding'
    )

    track_record_details = models.TextField(
        max_length=5000,
        blank=True,
        help_text='Describe the track record of this company here.'
    )

    # Offline use

    offline_capable = ExtendedYesNoField(
        help_text='Can this product be used offline?',
    )

    offline_use_description = models.TextField(
        max_length=5000,
        blank=True,
        help_text='Describe how this product can be used offline.'
    )

    # Artificial Intelligence

    uses_ai = ExtendedYesNoField(
        help_text='Does the product use AI?'
    )

    ai_uses_personal_data = ExtendedYesNoField(
        help_text='Does the AI use your personal data to make decisions about you?'
    )

    ai_is_transparent = ExtendedYesNoField(
        help_text='Does the company allow users to see how the AI works?'
    )

    ai_helptext = models.TextField(
        max_length=5000,
        blank=True,
        help_text='Helpful text around AI to show on the product page',

    )

    # administrative panels

    panels = Product.panels.copy()

    panels = insert_panels_after(
        panels,
        'General Product Details',
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
        'What is required to sign up',
        [
            MultiFieldPanel(
                [
                    FieldPanel('personal_data_collected'),
                    FieldPanel('biometric_data_collected'),
                    FieldPanel('social_data_collected'),
                ],
                heading='What data does it collect',
                classname='collapsible',
            ),
        ]
    )

    panels = insert_panels_after(
        panels,
        'How does it use this data',
        [
            MultiFieldPanel(
                [
                    FieldPanel('how_can_you_control_your_data'),
                    FieldPanel('data_control_policy_is_bad'),
                ],
                heading='How can you control your data',
                classname='collapsible',
            ),
            MultiFieldPanel(
                [
                    FieldPanel('company_track_record'),
                    FieldPanel('track_record_is_bad'),
                    FieldPanel('track_record_details'),
                ],
                heading='Company track record',
                classname='collapsible'
            ),
            MultiFieldPanel(
                [
                    FieldPanel('offline_capable'),
                    FieldPanel('offline_use_description'),
                ],
                heading='Offline use',
                classname='collapsible'
            ),
        ],
    )

    panels = insert_panels_after(
        panels,
        'Security',
        [
            MultiFieldPanel(
                [
                    FieldPanel('uses_ai'),
                    FieldPanel('ai_uses_personal_data'),
                    FieldPanel('ai_is_transparent'),
                    FieldPanel('ai_helptext'),
                ],
                heading='Artificial Intelligence',
                classname='collapsible'
            ),
        ],
    )

    def to_dict(self):
        model_dict = super().to_dict()
        model_dict['product_type'] = 'general'
        return model_dict


# Register this model class so that Product can "cast" properly
register_product_type(GeneralProduct)
