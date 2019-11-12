from datetime import datetime

from cloudinary import uploader
from cloudinary.models import CloudinaryField

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.forms import model_to_dict
from django.utils.text import slugify

from networkapi.buyersguide.fields import ExtendedYesNoField
from networkapi.buyersguide.validators import ValueListValidator
from networkapi.utility.images import get_image_upload_path

from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey

from wagtail.core.models import Orderable
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.snippets.models import register_snippet

from .utils import tri_to_quad


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
        blank=True,
    )

    title = models.CharField(
        max_length=256,
        blank=True,
    )

    author = models.CharField(
        max_length=256,
        blank=True,
    )

    snippet = models.TextField(
        max_length=5000,
        blank=True,
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
    description = models.TextField(
        max_length=300,
        help_text='Description of the product category. Max. 300 characters.',
        blank=True
    )

    featured = models.BooleanField(
        default=False,
        help_text='Featured category will appear first on Buyer\'s Guide site nav'
    )

    hidden = models.BooleanField(
        default=False,
        help_text='Hidden categories will not appear in the Buyer\'s Guide site nav at all'
    )

    slug = models.SlugField(
        blank=True,
        help_text='A URL-friendly version of the product name. This is an auto-generated field.'
    )

    @property
    def published_product_count(self):
        return Product.objects.filter(product_category=self, draft=False).count()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(BuyersGuideProductCategory, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Buyers Guide Product Category"
        verbose_name_plural = "Buyers Guide Product Categories"


class Product(ClusterableModel):
    """
    A thing you can buy in stores and our review of it
    """

    draft = models.BooleanField(
        help_text='When checked, this product will only show for CMS-authenticated users',
        default=True,
    )

    adult_content = models.BooleanField(
        help_text='When checked, product thumbnail will appear blurred as well as have an 18+ badge on it',
        default=False,
    )

    review_date = models.DateField(
        help_text='Review date of this product',
    )

    @property
    def is_current(self):
        d = self.review_date
        review = datetime(d.year, d.month, d.day)
        cutoff = datetime(2019, 6, 1)
        return cutoff < review

    name = models.CharField(
        max_length=100,
        help_text='Name of Product',
        blank=True,
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
        blank=True,
    )

    product_category = models.ManyToManyField(
        BuyersGuideProductCategory,
        related_name='product',
        blank=True
    )

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

    meets_minimum_security_standards = models.BooleanField(
        null=True,
        help_text='Does this product meet minimum security standards?',
    )

    # Minimum security standards (stars)

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

    share_data = models.BooleanField(  # TO BE REMOVED
        null=True,
        help_text='Does the maker share data with other companies?',
    )

    share_data_helptext = models.TextField(  # TO BE REMOVED
        max_length=5000,
        blank=True
    )

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

    # How it handles privacy

    how_does_it_share = models.CharField(
        max_length=5000,
        help_text='How does this product handle data?',
        blank=True
    )

    delete_data = models.BooleanField(  # TO BE REMOVED
        null=True,
        help_text='Can you request data be deleted?',
    )

    delete_data_helptext = models.TextField(  # TO BE REMOVED
        max_length=5000,
        blank=True
    )

    parental_controls = ExtendedYesNoField(
        null=True,
        help_text='Are there rules for children?',
    )

    child_rules_helptext = models.TextField(  # TO BE REMOVED
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

    user_friendly_privacy_policy = ExtendedYesNoField(
        help_text='Does this product have a user-friendly privacy policy?'
    )

    user_friendly_privacy_policy_helptext = models.TextField(
        max_length=5000,
        blank=True
    )

    """
    privacy_policy_links =  one to many, defined in PrivacyPolicyLink
    """

    worst_case = models.CharField(
        max_length=5000,
        help_text="What's the worst thing that could happen by using this product?",
        blank=True,
    )

    PP_CHOICES = (  # TO BE REMOVED
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

    privacy_policy_reading_level = models.CharField(  # TO BE REMOVED IN FAVOUR OF USER_FRIENDLY_PRIVACY_POLICY
        choices=PP_CHOICES,
        default='0',
        max_length=2,
    )

    privacy_policy_url = models.URLField(  # TO BE REMOVED IN FAVOUR OF PRIVACY_POLICY_LINKS
        max_length=2048,
        help_text='Link to privacy policy',
        blank=True
    )

    privacy_policy_reading_level_url = models.URLField(  # TO BE REMOVED
        max_length=2048,
        help_text='Link to privacy policy reading level',
        blank=True
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

    updates = models.ManyToManyField(Update, related_name='products', blank=True)

    # comments are not a model field, but are "injected" on the product page instead

    related_products = models.ManyToManyField('self', related_name='rps', blank=True, symmetrical=False)

    # ---

    if settings.USE_CLOUDINARY:
        image_field = FieldPanel('cloudinary_image')
    else:
        image_field = FieldPanel('image')

    # List of fields to show in admin to hide the image/cloudinary_image field. There's probably a better way to do
    # this using `_meta.get_fields()`. To be refactored in the future.
    panels = [
        MultiFieldPanel(
            [
                FieldPanel('draft'),
            ],
            heading="Publication status"
        ),
        MultiFieldPanel(
            [
                FieldPanel('adult_content'),
                FieldPanel('review_date'),
                FieldPanel('name'),
                FieldPanel('company'),
                FieldPanel('product_category'),
                FieldPanel('blurb'),
                FieldPanel('url'),
                FieldPanel('price'),
                image_field,
                FieldPanel('meets_minimum_security_standards')
            ],
            heading="General Product Details"
        ),
        MultiFieldPanel(
            [
                FieldPanel('uses_encryption'),
                FieldPanel('uses_encryption_helptext'),
                FieldPanel('security_updates'),
                FieldPanel('security_updates_helptext'),
                FieldPanel('strong_password'),
                FieldPanel('strong_password_helptext'),
                FieldPanel('manage_vulnerabilities'),
                FieldPanel('manage_vulnerabilities_helptext'),
                FieldPanel('privacy_policy'),
                FieldPanel('privacy_policy_helptext'),  # NEED A "clear" MIGRATION
                FieldPanel('share_data'),
                FieldPanel('share_data_helptext'),

                # DEPRECATED AND WILL BE REMOVED
                FieldPanel('privacy_policy_url'),
                FieldPanel('privacy_policy_reading_level'),
                FieldPanel('privacy_policy_reading_level_url'),
            ],
            heading="Minimum Security Standards",
            classname="collapsible"
        ),
        MultiFieldPanel(
            [
                FieldPanel('camera_device'),
                FieldPanel('camera_app'),
                FieldPanel('microphone_device'),
                FieldPanel('microphone_app'),
                FieldPanel('location_device'),
                FieldPanel('location_app'),
            ],
            heading="Can it snoop?",
            classname="collapsible"
        ),
        MultiFieldPanel(
            [
                FieldPanel('how_does_it_share'),
                FieldPanel('delete_data'),
                FieldPanel('delete_data_helptext'),
                FieldPanel('parental_controls'),
                FieldPanel('collects_biometrics'),
                FieldPanel('collects_biometrics_helptext'),
                FieldPanel('user_friendly_privacy_policy'),
                FieldPanel('user_friendly_privacy_policy_helptext'),
                FieldPanel('worst_case'),
            ],
            heading="How does it handle privacy",
            classname="collapsible"
        ),
        MultiFieldPanel(
            [
                InlinePanel(
                    'privacy_policy_links',
                    label='link',
                    min_num=1,
                    max_num=3,
                ),
            ],
            heading="Privacy policy links",
            classname="collapsible"
        ),
        MultiFieldPanel(
            [
                FieldPanel('phone_number'),
                FieldPanel('live_chat'),
                FieldPanel('email'),
                FieldPanel('twitter'),
            ],
            heading="Ways to contact the company",
            classname="collapsible"
        ),
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
        """
        Rather than rendering products based on the instance object,
        we serialize the product to a dictionary, and instead render
        the template based on that.

        NOTE: if you add indirect fields like Foreign/ParentalKey or
              @property definitions, those needs to be added!
        """
        model_dict = model_to_dict(self)

        model_dict['votes'] = self.votes
        model_dict['slug'] = self.slug
        model_dict['delete_data'] = tri_to_quad(self.delete_data)

        # TODO: remove these two entries
        model_dict['numeric_reading_grade'] = self.numeric_reading_grade
        model_dict['reading_grade'] = self.reading_grade

        # model_to_dict does NOT capture related fields or @properties!
        model_dict['privacy_policy_links'] = list(self.privacy_policy_links.all())
        model_dict['is_current'] = self.is_current

        return model_dict

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        models.Model.save(self, *args, **kwargs)

    def __str__(self):
        return str(self.name)


@register_snippet
class ProductPrivacyPolicyLink(Orderable, models.Model):
    product = ParentalKey(
        'Product',
        related_name='privacy_policy_links',
        on_delete=models.CASCADE
    )

    label = models.CharField(
        max_length=500,
        help_text='Label for this link on the product page'
    )

    url = models.URLField(
        max_length=2048,
        help_text='Privacy policy URL',
        blank=True
    )

    def __str__(self):
        return f'{self.product.name}: {self.label} ({self.url})'

    class Meta:
        verbose_name = "Buyers Guide Product Privacy Policy link"
        verbose_name_plural = "Buyers Guide Product Privacy Policy links"


# We want to delete the product image when the product is removed
@receiver(pre_delete, sender=Product)
def delete_image(sender, instance, **kwargs):
    # We want to keep our review app placeholders
    if settings.HEROKU_APP_NAME:
        pass
    else:
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
