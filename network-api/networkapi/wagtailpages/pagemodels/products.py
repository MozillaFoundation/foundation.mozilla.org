from django.db import models

from wagtail.core.models import Page

from networkapi.buyersguide.fields import ExtendedYesNoField
from networkapi.buyersguide.pagemodels.cloudinary_image_field import (
    CloudinaryField
)
from networkapi.wagtailpages.pagemodels.mixin.foundation_metadata import (
    FoundationMetadataPageMixin
)


class ProductPage(FoundationMetadataPageMixin, Page):
    """
    ProductPage is the superclass that SoftwareProductPage and
    GeneralProductPage inherit from. This should not be an abstract
    model as we need it to connect the two page types together.
    """

    privacy_ding = models.BooleanField(
        help_text='Tick this box if privacy is not included for this product',
        default=False,
    )
    adult_content = models.BooleanField(
        help_text='When checked, product thumbnail will appear blurred as well as have an 18+ badge on it',
        default=False,
    )
    uses_wifi = models.BooleanField(
        help_text='Does this product rely on WiFi connectivity?',
        default=False,
    )
    uses_bluetooth = models.BooleanField(
        help_text='Does this product rely on Bluetooth connectivity?',
        default=False,
    )
    review_date = models.DateField(
        help_text='Review date of this product',
    )
    company = models.CharField(
        max_length=100,
        help_text='Name of Company',
        blank=True,
    )
    # product_category = # TODO: Convert the ManyToMany field to an Orderable
    # Keeping code commented out for quick reference in a future ticket
    # models.ManyToManyField(
    #     'buyersguide.BuyersGuideProductCategory',
    #     related_name='pniproduct',
    #     blank=True
    # )
    blurb = models.TextField(
        max_length=5000,
        help_text='Description of the product',
        blank=True
    )
    url = models.URLField(
        max_length=2048,
        help_text='Link to this product page',
        blank=True,
    )
    price = models.CharField(
        max_length=100,
        help_text='Price',
        blank=True,
    )
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Image representing this product',
    )
    cloudinary_image = CloudinaryField(
        help_text='Image representing this product - hosted on Cloudinary',
        blank=True,
        verbose_name='image',
        folder='foundationsite/buyersguide',
        use_filename=True
    )
    worst_case = models.CharField(
        max_length=5000,
        help_text="What's the worst thing that could happen by using this product?",
        blank=True,
    )

    # What is required to sign up?
    signup_requires_email = ExtendedYesNoField(
        help_text='Does this product requires providing an email address in order to sign up?'
    )

    signup_requires_phone = ExtendedYesNoField(
        help_text='Does this product requires providing a phone number in order to sign up?'
    )

    signup_requires_third_party_account = ExtendedYesNoField(
        help_text='Does this product require a third party account in order to sign up?'
    )

    signup_requirement_explanation = models.TextField(
        max_length=5000,
        blank=True,
        help_text='Describe the particulars around sign-up requirements here.'
    )

    # How does it use this data?

    how_does_it_use_data_collected = models.TextField(
        max_length=5000,
        blank=True,
        help_text='How does this product use the data collected?'
    )

    data_collection_policy_is_bad = models.BooleanField(
        default=False,
        verbose_name='Privacy ding'
    )

    # Privacy policy

    user_friendly_privacy_policy = ExtendedYesNoField(
        help_text='Does this product have a user-friendly privacy policy?'
    )

    # Minimum security standards

    show_ding_for_minimum_security_standards = models.BooleanField(
        default=False,
        verbose_name="Privacy ding"
    )

    meets_minimum_security_standards = models.BooleanField(
        null=True,
        help_text='Does this product meet our minimum security standards?',
    )

    uses_encryption = ExtendedYesNoField(
        help_text='Does the product use encryption?',
    )

    uses_encryption_helptext = models.TextField(
        max_length=5000,
        blank=True
    )

    security_updates = ExtendedYesNoField(
        help_text='Security updates?',
    )

    security_updates_helptext = models.TextField(
        max_length=5000,
        blank=True
    )

    strong_password = ExtendedYesNoField()

    strong_password_helptext = models.TextField(
        max_length=5000,
        blank=True
    )

    manage_vulnerabilities = ExtendedYesNoField(
        help_text='Manages security vulnerabilities?',
    )

    manage_vulnerabilities_helptext = models.TextField(
        max_length=5000,
        blank=True
    )

    privacy_policy = ExtendedYesNoField(
        help_text='Does this product have a privacy policy?'
    )

    privacy_policy_helptext = models.TextField(  # REPURPOSED: WILL REQUIRE A 'clear' MIGRATION
        max_length=5000,
        blank=True
    )

    """
    privacy_policy_links = one to many, defined in PrivacyPolicyLink
    """

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

    # updates = TODO: Convert the ManyToMany field to an Orderable
    # models.ManyToManyField(
    #     'buyersguide.Update',
    #     related_name='pniproduct',
    #     blank=True
    # )

    class Meta:
        verbose_name = "Product Page"


class SoftwareProductPage(ProductPage):

    class Meta:
        verbose_name = "Software Product Page"


class GeneralProductPage(ProductPage):

    class Meta:
        verbose_name = "General Product Page"
