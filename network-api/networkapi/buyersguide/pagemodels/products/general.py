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

    # How does it use this data?

    how_does_it_use_data_collected = models.TextField(
        max_length=5000,
        blank=True,
        help_text='How does this product use the data collected?'
    )

    data_collection_policy_is_bad = models.BooleanField(
        default=False,
    )

    how_can_you_control_your_data = models.TextField(
        max_length=5000,
        blank=True,
        help_text='How does this product let you control your data?'
    )

    data_control_policy_is_bad = models.BooleanField(
        default=False,
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
        help_text='Does the product use AI?',
    )

    ai_uses_personal_data = ExtendedYesNoField(
        help_text='Does the AI use your personal data to make decisions about you?',
    )

    ai_is_transparent = ExtendedYesNoField(
        help_text='Does the company allow users to see how the AI works?',
    )

    ai_helptext = models.TextField(
        max_length=5000,
        blank=True,
        help_text='Helpful text around AI to show on the product page',
    )

    # How to contact the company

    phone_number = models.CharField(
        max_length=100,
        help_text='Phone Number',
        blank=True,
    )

    live_chat = models.CharField(
        max_length=100,
        help_text='Live Chat',
        blank=True,
    )

    email = models.CharField(
        max_length=100,
        help_text='Email',
        blank=True,
    )

    twitter = models.CharField(
        max_length=100,
        help_text='Twitter username',
        blank=True,
    )

    # administrative panels

    panels = Product.panels.copy()

    panels = insert_panels_after(
        panels,
        'What is the worst that could happen',
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
                    FieldPanel('how_does_it_use_data_collected'),
                    FieldPanel('data_collection_policy_is_bad'),
                    FieldPanel('how_can_you_control_your_data'),
                    FieldPanel('data_control_policy_is_bad'),
                ],
                heading='Data collection and control',
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
            MultiFieldPanel(
                [
                    FieldPanel('phone_number'),
                    FieldPanel('live_chat'),
                    FieldPanel('email'),
                    FieldPanel('twitter'),
                ],
                heading='Ways to contact the company',
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
