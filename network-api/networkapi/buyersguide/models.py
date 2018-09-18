from django.db import models
from networkapi.utility.images import get_image_upload_path
# from wagtail.snippets.models import register_snippet


def get_product_image_upload_path(instance, filename):
    return get_image_upload_path(
        app_name='buyersguide',
        prop_name='name',
        instance=instance,
        current_filename=filename
    )


# https://docs.google.com/document/d/1jtWOVqH20qMYRSwvb2rHzPNTrWIoPs8EbWR25r9iyi4/edit

class Product(models.Model):
    """
    A thing you can buy in stores and our review of it
    """

    name = models.CharField(
        max_length=100,
        help_text='Name of Product',
        blank="True",
    )

    company = models.CharField(
        max_length=100,
        help_text='Name of Company',
        blank="True",
    )

    blurb = models.TextField(
        max_length=5000,
        help_text='Description of the product',
        blank="True"
    )

    url = models.URLField(
        max_length=2048,
        help_text='Link to this product page',
        blank="True",
    )

    price = models.CharField(
        max_length=100,
        help_text='Price',
        blank="True",
    )

    image = models.FileField(
        max_length=2048,
        help_text='Image representing this prodct',
        upload_to=get_product_image_upload_path,
        blank=True,
    )

    # Can it spy on me?

    camera = models.NullBooleanField(
        help_text='Does this product have or access a camera?',
    )

    microphone = models.NullBooleanField(
        help_text='Does this product have or access a microphone?',
    )

    location = models.NullBooleanField(
        help_text='Does this product access your location?',
    )

    # What does it know about me?

    uses_encryption = models.NullBooleanField(
        help_text='Does the product use encryption?',
    )

    privacy_policy = models.URLField(
        help_text='Link to privacy policy for this product',
        max_length=2048,
        blank="True",
    )

    share_data = models.NullBooleanField(
        help_text='Does the maker share data with other companies?',
    )

    # Can I control it?

    must_change_default_password = models.NullBooleanField(
        help_text='Must change a default password?',
    )

    security_updates = models.NullBooleanField(
        help_text='Security updates?',
    )

    need_account = models.NullBooleanField(
        help_text='Do you need an account to use this product?',
    )

    delete_data = models.NullBooleanField(
        help_text='Can you request data be deleted?',
    )

    child_rules = models.NullBooleanField(
        help_text='Are there rules for children?',
    )

    # Company shows it cares about its customers?

    manage_security = models.NullBooleanField(
        help_text='Manages security vulnerabilities?',
    )

    customer_support_easy = models.NullBooleanField(
        help_text='Makes it easy to contact customer support?',
    )

    phone_number = models.CharField(
        max_length=100,
        help_text='Phone Number',
        blank="True",
    )

    live_chat = models.CharField(
        max_length=100,
        help_text='Live Chat',
        blank="True",
    )

    email = models.CharField(
        max_length=100,
        help_text='Email',
        blank="True",
    )

    # What could happen if something went wrong?

    worst_case = models.CharField(
        max_length=5000,
        help_text="What's the worst thing that could happen by using this product?",
        blank="True",
    )

    # objects = HighlightQuerySet.as_manager()

    def __str__(self):
        return str(self.name)
