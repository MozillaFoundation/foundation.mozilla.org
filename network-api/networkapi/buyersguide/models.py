import re

from cloudinary import uploader
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.forms import model_to_dict
from django.utils.text import slugify
from wagtail.admin.edit_handlers import MultiFieldPanel, FieldPanel

from networkapi.buyersguide.validators import ValueListValidator
from networkapi.utility.images import get_image_upload_path
from wagtail.snippets.models import register_snippet

from cloudinary.models import CloudinaryField


def get_product_image_upload_path(instance, filename):
    return get_image_upload_path(
        app_name='buyersguide',
        prop_name='name',
        instance=instance,
        current_filename=filename
    )


# Override the default 'public_id' to upload all images to the buyers guide directory on Cloudinary
class CloudinaryImageField(CloudinaryField):
    def upload_options(self, model_instance):
        return {
            'folder': 'foundationsite/buyersguide',
            'use_filename': True,
        }


# https://docs.google.com/document/d/1jtWOVqH20qMYRSwvb2rHzPNTrWIoPs8EbWR25r9iyi4/edit

class Update(models.Model):
    source = models.URLField(
        max_length=2048,
        help_text='Link to source',
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


@register_snippet
class BuyersGuideProductCategory(models.Model):
    """
    A simple category class for use with Buyers Guide products,
    registered as snippet so that we can moderate them if and
    when necessary.
    """
    name = models.CharField(max_length=100)

    @property
    def websafe_name(self):
        return re.sub(r"[ \W]+", "-", self.name).lower()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Buyers Guide Product Category"
        verbose_name_plural = "Buyers Guide Product Categories"


class Product(models.Model):
    """
    A thing you can buy in stores and our review of it
    """

    name = models.CharField(
        max_length=100,
        help_text='Name of Product',
        blank="True",
    )

    slug = models.CharField(
        max_length=256,
        help_text='slug used in urls',
        blank=True,
        default=None,
        editable=False
    )

    company = models.CharField(
        max_length=100,
        help_text='Name of Company',
        blank="True",
    )

    product_category = models.ManyToManyField(
        BuyersGuideProductCategory,
        related_name='product',
        blank=True
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
        help_text='Image representing this product',
        upload_to=get_product_image_upload_path,
        blank=True,
    )

    cloudinary_image = CloudinaryImageField(
        help_text='Image representing this product - hosted on Cloudinary',
        blank=True,
        verbose_name='image',
    )

    meets_minimum_security_standards = models.NullBooleanField(
        help_text='Does this product meet minimum security standards?',
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
        max_length=2048,
        help_text='Link to privacy policy',
        blank="True"
    )

    privacy_policy_reading_level = models.CharField(
        choices=PP_CHOICES,
        default='0',
        max_length=2,
    )

    privacy_policy_reading_level_url = models.URLField(
        max_length=2048,
        help_text='Link to privacy policy reading level',
        blank="True"
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

    updates = models.ManyToManyField(Update, related_name='products', blank=True)

    related_products = models.ManyToManyField('self', related_name='rps', blank=True, symmetrical=False)

    if settings.USE_CLOUDINARY:
        image_field = FieldPanel('cloudinary_image')
    else:
        image_field = FieldPanel('image')

    # List of fields to show in admin to hide the image/cloudinary_image field. There's probably a better way to do
    # this using `_meta.get_fields()`. To be refactored in the future.
    panels = [
        MultiFieldPanel([
            FieldPanel('name'),
            FieldPanel('company'),
            FieldPanel('product_category'),
            FieldPanel('blurb'),
            FieldPanel('url'),
            FieldPanel('price'),
            image_field,
            FieldPanel('meets_minimum_security_standards')
        ],
            heading="Product General Details"
        ),
        MultiFieldPanel([
            FieldPanel('camera_device'),
            FieldPanel('camera_app'),
            FieldPanel('microphone_device'),
            FieldPanel('microphone_app'),
            FieldPanel('location_device'),
            FieldPanel('location_app'),
        ],
            heading="Can it spy on me?",
            classname="collapsible"
        ),
        MultiFieldPanel([
            FieldPanel('uses_encryption'),
            FieldPanel('uses_encryption_helptext'),
            FieldPanel('privacy_policy_url'),
            FieldPanel('privacy_policy_reading_level'),
            FieldPanel('privacy_policy_reading_level_url'),
            FieldPanel('privacy_policy_helptext'),
            FieldPanel('share_data'),
            FieldPanel('share_data_helptext'),
        ],
            heading="What does it know about me?",
            classname="collapsible"
        ),
        MultiFieldPanel([
            FieldPanel('must_change_default_password'),
            FieldPanel('must_change_default_password_helptext'),
            FieldPanel('security_updates'),
            FieldPanel('security_updates_helptext'),
            FieldPanel('delete_data'),
            FieldPanel('delete_data_helptext'),
            FieldPanel('child_rules'),
            FieldPanel('child_rules_helptext'),
        ],
            heading="Can I control it?",
            classname="collapsible"
        ),
        MultiFieldPanel([
            FieldPanel('manage_security'),
            FieldPanel('manage_security_helptext'),
            FieldPanel('phone_number'),
            FieldPanel('live_chat'),
            FieldPanel('email'),
            FieldPanel('twitter'),
        ],
            heading="Company shows it cares about its customers?",
            classname="collapsible"
        ),
        FieldPanel('worst_case'),
        FieldPanel('updates'),
        FieldPanel('related_products'),
    ]

    @property
    def votes(self):
        votes = {}
        confidence_vote_breakdown = {}
        creepiness = {'vote_breakdown': {}}

        try:
            # Get vote QuerySets
            creepiness_votes = self.range_product_votes.get(attribute='creepiness')
            confidence_votes = self.boolean_product_votes.get(attribute='confidence')

            # Aggregate the Creepiness votes
            creepiness['average'] = creepiness_votes.average
            for vote_breakdown in creepiness_votes.rangevotebreakdown_set.all():
                creepiness['vote_breakdown'][str(vote_breakdown.bucket)] = vote_breakdown.count

            # Aggregate the confidence votes
            for boolean_vote_breakdown in confidence_votes.booleanvotebreakdown_set.all():
                confidence_vote_breakdown[str(boolean_vote_breakdown.bucket)] = boolean_vote_breakdown.count

            # Build + return the votes dict
            votes['creepiness'] = creepiness
            votes['confidence'] = confidence_vote_breakdown
            votes['total'] = BooleanVote.objects.filter(product=self).count()
            return votes

        except ObjectDoesNotExist:
            # There's no aggregate data available yet, return None
            return None

    @property
    def numeric_reading_grade(self):
        try:
            return int(self.privacy_policy_reading_level)
        except ValueError:
            return 0

    @property
    def reading_grade(self):
        val = self.numeric_reading_grade
        if val == 0:
            return 0
        if val <= 8:
            return 'Middle school'
        if val <= 12:
            return 'High school'
        if val <= 16:
            return 'College'
        return 'Grad school'

    def to_dict(self):
        model_dict = model_to_dict(self)
        model_dict['votes'] = self.votes
        model_dict['slug'] = self.slug
        model_dict['numeric_reading_grade'] = self.numeric_reading_grade
        model_dict['reading_grade'] = self.reading_grade
        return model_dict

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        models.Model.save(self, *args, **kwargs)

    def __str__(self):
        return str(self.name)


# We want to delete the product image when the product is removed
@receiver(pre_delete, sender=Product)
def delete_image(sender, instance, **kwargs):
    if instance.cloudinary_image:
        uploader.destroy(instance.cloudinary_image.public_id, invalidate=True)


class ProductVote(models.Model):
    votes = models.IntegerField(
        default=0
    )

    class Meta:
        abstract = True


class RangeProductVote(ProductVote):
    attribute = models.CharField(
        max_length=100,
        validators=[
            ValueListValidator(valid_values=['creepiness'])
        ]
    )
    average = models.IntegerField(
        validators=(
            MinValueValidator(1),
            MaxValueValidator(100)
        )
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='range_product_votes',
    )


class BooleanProductVote(ProductVote):
    attribute = models.CharField(
        max_length=100,
        validators=[
            ValueListValidator(valid_values=['confidence'])
        ]
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='boolean_product_votes'
    )


class VoteBreakdown(models.Model):
    count = models.IntegerField(
        default=0
    )

    class Meta:
        abstract = True


class BooleanVoteBreakdown(VoteBreakdown):
    product_vote = models.ForeignKey(
        BooleanProductVote,
        on_delete=models.CASCADE
    )
    bucket = models.IntegerField(
        validators=[
            ValueListValidator(
                valid_values=[0, 1]
            )
        ]
    )


class RangeVoteBreakdown(VoteBreakdown):
    product_vote = models.ForeignKey(
        RangeProductVote,
        on_delete=models.CASCADE
    )
    bucket = models.IntegerField(
        validators=[
            ValueListValidator(
                valid_values=[0, 1, 2, 3, 4]
            )
        ]
    )


class Vote(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class BooleanVote(Vote):
    attribute = models.CharField(
        max_length=100,
        validators=[
            ValueListValidator(valid_values=['confidence'])
        ]
    )
    value = models.BooleanField()


class RangeVote(Vote):
    attribute = models.CharField(
        max_length=100,
        validators=[
            ValueListValidator(valid_values=['creepiness'])
        ]
    )
    value = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100)
        ]
    )
