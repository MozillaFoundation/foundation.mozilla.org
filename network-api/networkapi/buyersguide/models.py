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
        help_text='Price range',
        blank="True",
    )
    image = models.FileField(
        max_length=2048,
        help_text='Image representing this prodct',
        upload_to=get_product_image_upload_path,
        blank=True,
    )
    camera = models.NullBooleanField(
        help_text='Does this product have or access a camera?',
    )
    microphone = models.NullBooleanField(
        help_text='Does this product have or access a microphone?',
    )
    location = models.NullBooleanField(
        help_text='Does this product access your location?',
    )
    need_account = models.NullBooleanField(
        help_text='Do you need an account to use this product?',
    )
    privacy_controls = models.NullBooleanField(
        help_text='Do users have access to privacy controls?',
    )
    delete_data = models.NullBooleanField(
        help_text='Can you request data be deleted?',
    )
    share_data = models.NullBooleanField(
        help_text='Does the maker share data with other companies?',
    )
    child_rules = models.NullBooleanField(
        help_text='Are there rules for children?',
    )
    privacy_policy = models.URLField(
        help_text='Link to privacy policy for this product',
        max_length=2048,
        blank="True",
    )
    worst_case = models.CharField(
        max_length=5000,
        help_text="What's the worst thing that could happen by using this product?",
        blank="True",
    )

    # objects = HighlightQuerySet.as_manager()

    def __str__(self):
        return str(self.name)
