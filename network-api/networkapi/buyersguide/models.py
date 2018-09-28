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

class Update(models.Model):
    source = models.CharField(
        max_length=256,
        blank="True",
    )

    title = models.CharField(
        max_length=256,
        blank="True",
    )

    author = models.CharField(
        max_length=256,
        blank="True",
    )

    snippet = models.TextField(
        max_length=5000,
        blank="True",
    )

    def __str__(self):
        return self.title


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

    camera_device = models.NullBooleanField(
        help_text='Does this device have or access a camera?',
    )

    camera_app = models.NullBooleanField(
        help_text='Does the app have or access a camera?',
    )

    microphone_device = models.NullBooleanField(
        help_text='Does this Device have or access a microphone?',
    )

    microphone_app = models.NullBooleanField(
        help_text='Does this app have or access a microphone?',
    )

    location_device = models.NullBooleanField(
        help_text='Does this product access your location?',
    )

    location_app = models.NullBooleanField(
        help_text='Does this app access your location?',
    )

    # What does it know about me?

    uses_encryption = models.NullBooleanField(
        help_text='Does the product use encryption?',
    )

    uses_encryption_helptext = models.TextField(
        max_length=5000,
        blank="True"
    )

    PP_CHOICES = (
        ('0', 'Can\'t Determine'),
        ('7', 'Grade 7'),
        ('8', 'Grade 8'),
        ('9', 'Grade 9'),
        ('10', 'Grade 10'),
        ('11', 'Grade 11'),
        ('12', 'Grade 12'),
        ('13', 'Grade 13'),
        ('14', 'Grade 14'),
        ('15', 'Grade 15'),
        ('16', 'Grade 16'),
        ('17', 'Grade 17'),
        ('18', 'Grade 18'),
        ('19', 'Grade 19'),
    )

    privacy_policy_url = models.URLField(
        blank="True"
    )

    privacy_policy_reading_level = models.CharField(
        choices=PP_CHOICES,
        default='0',
        max_length=2,
    )

    privacy_policy_helptext = models.TextField(
        max_length=5000,
        blank="True"
    )

    share_data = models.NullBooleanField(
        help_text='Does the maker share data with other companies?',
    )

    share_data_helptext = models.TextField(
        max_length=5000,
        blank="True"
    )

    # Can I control it?

    must_change_default_password = models.NullBooleanField(
        help_text='Must change a default password?',
    )

    must_change_default_password_helptext = models.TextField(
        max_length=5000,
        blank="True"
    )

    security_updates = models.NullBooleanField(
        help_text='Security updates?',
    )

    security_updates_helptext = models.TextField(
        max_length=5000,
        blank="True"
    )

    need_account = models.NullBooleanField(
        help_text='Do you need an account to use this product?',
    )

    need_account_helptext = models.TextField(
        max_length=5000,
        blank="True"
    )

    delete_data = models.NullBooleanField(
        help_text='Can you request data be deleted?',
    )

    delete_data_helptext = models.TextField(
        max_length=5000,
        blank="True"
    )

    child_rules = models.NullBooleanField(
        help_text='Are there rules for children?',
    )

    child_rules_helptext = models.TextField(
        max_length=5000,
        blank="True"
    )

    # Company shows it cares about its customers?

    manage_security = models.NullBooleanField(
        help_text='Manages security vulnerabilities?',
    )

    manage_security_helptext = models.TextField(
        max_length=5000,
        blank="True"
    )

    customer_support_easy_helptext = models.TextField(
        max_length=5000,
        blank="True"
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

    twitter = models.CharField(
        max_length=100,
        help_text='Twitter username',
        blank="True",
    )

    # What could happen if something went wrong?

    worst_case = models.CharField(
        max_length=5000,
        help_text="What's the worst thing that could happen by using this product?",
        blank="True",
    )

    updates = models.ManyToManyField(Update, related_name='products', null=True, blank=True)

    related_products = models.ManyToManyField('self', related_name='rps', null=True, blank=True)

    # objects = HighlightQuerySet.as_manager()

    def __str__(self):
        return str(self.name)
