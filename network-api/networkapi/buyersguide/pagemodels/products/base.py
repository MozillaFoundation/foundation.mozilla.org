from datetime import datetime

from cloudinary import uploader

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.forms import model_to_dict
from django.utils.text import slugify

from networkapi.buyersguide.fields import ExtendedYesNoField

from modelcluster.models import ClusterableModel

from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel

from ..cloudinary_image_field import CloudinaryField
from ..get_product_image_upload_path import get_product_image_upload_path
from ..get_product_vote_information import get_product_vote_information

if settings.USE_CLOUDINARY:
    image_field = FieldPanel('cloudinary_image')
else:
    image_field = FieldPanel('image')

# Let's figure out whether we can refactor this to its own file.
product_panels = [
    MultiFieldPanel(
        [
            FieldPanel('draft'),
        ],
        heading="Publication status",
        classname="collapsible"
    ),

    # core information
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
        heading="General Product Details",
        classname="collapsible"
    ),

    # minimum security standard
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
        ],
        heading="Minimum Security Standards for general products",
        classname="collapsible"
    ),
    # Data sharing
    MultiFieldPanel(
        [
            FieldPanel('share_data'),
            FieldPanel('share_data_helptext'),
            FieldPanel('how_does_it_share'),
        ],
        heading="How does it handle data sharing",
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
            FieldPanel('worst_case'),
        ],
        heading="What's the worst that could happen",
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

registered_product_types = list()


def register_product_type(ModelClass):
    registered_product_types.append(ModelClass)


class Product(ClusterableModel):
    """
    A product that may not have privacy included.
    """
    @property
    def specific(self):
        for Type in registered_product_types:
            try:
                return Type.objects.get(slug=self.slug)
            except ObjectDoesNotExist:
                pass
        return self

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
        'buyersguide.BuyersGuideProductCategory',
        related_name='pniproduct',
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

    cloudinary_image = CloudinaryField(
        help_text='Image representing this product - hosted on Cloudinary',
        blank=True,
        verbose_name='image',
        folder='foundationsite/buyersguide',
        use_filename=True
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

    # How it handles privacy

    share_data = models.BooleanField(  # TO BE REMOVED?
        null=True,
        help_text='Does the maker share data with other companies?',
    )

    share_data_helptext = models.TextField(  # TO BE REMOVED?
        max_length=5000,
        blank=True
    )

    how_does_it_share = models.CharField(
        max_length=5000,
        help_text='How does this product handle data?',
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

    updates = models.ManyToManyField(
        'buyersguide.Update',
        related_name='pniproduct',
        blank=True
    )

    # comments are not a model field, but are "injected" on the product page instead

    related_products = models.ManyToManyField(
        'self',
        related_name='related_pniproduct',
        blank=True,
        symmetrical=False
    )

    # List of fields to show in admin to hide the image/cloudinary_image field. There's probably a better way to do
    # this using `_meta.get_fields()`. To be refactored in the future.
    panels = product_panels

    @property
    def is_current(self):
        d = self.review_date
        review = datetime(d.year, d.month, d.day)
        cutoff = datetime(2019, 6, 1)
        return cutoff < review

    @property
    def votes(self):
        return get_product_vote_information(self)

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

        # model_to_dict does NOT capture related fields or @properties!
        model_dict['privacy_policy_links'] = list(self.privacy_policy_links.all())
        model_dict['is_current'] = self.is_current

        return model_dict

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        models.Model.save(self, *args, **kwargs)

    def __str__(self):
        return f'{self.name} ({self.company})'

    class Meta:
        # use oldest-first ordering
        ordering = [
            'id'
        ]


# We want to delete the product image when the product is removed
@receiver(pre_delete, sender=Product)
def delete_image(sender, instance, **kwargs):
    # We want to keep our review app placeholders
    if settings.REVIEW_APP:
        pass
    else:
        if instance.cloudinary_image:
            uploader.destroy(instance.cloudinary_image.public_id, invalidate=True)
