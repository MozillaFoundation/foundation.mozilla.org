from datetime import date, datetime

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


class RelatedProductFieldPanel(FieldPanel):
    """
    This is a custom field panel for listing related products in a regular
    product's admin view - rather than showing all entries, a large number
    of products should be ignored for cross-linking purposes. See the
    "def get_related_products(self):" function in the Product class, below,
    for more details on the queryset it returns.
    """
    def on_form_bound(self):
        instance = self.model
        self.form.fields['related_products'].queryset = instance.get_related_products(instance)
        super().on_form_bound()


# Let's figure out whether we can refactor this to its own file.
product_panels = [
    MultiFieldPanel(
        [
            FieldPanel('draft'),
        ],
        heading='Publication status',
        classname='collapsible'
    ),
    # core information
    MultiFieldPanel(
        [
            FieldPanel('privacy_ding'),
            FieldPanel('adult_content'),
            FieldPanel('uses_wifi'),
            FieldPanel('uses_bluetooth'),
            FieldPanel('review_date'),
            FieldPanel('name'),
            FieldPanel('company'),
            FieldPanel('product_category'),
            FieldPanel('blurb'),
            FieldPanel('url'),
            FieldPanel('price'),
            image_field,
        ],
        heading='General Product Details',
        classname='collapsible'
    ),
    MultiFieldPanel(
        [
            FieldPanel('worst_case'),
        ],
        heading='What is the worst that could happen',
        classname='collapsible'
    ),
    MultiFieldPanel(
        [
            FieldPanel('signup_requires_email'),
            FieldPanel('signup_requires_phone'),
            FieldPanel('signup_requires_third_party_account'),
            FieldPanel('signup_requirement_explanation'),
        ],
        heading='What is required to sign up',
        classname='collapsible'
    ),
    MultiFieldPanel(
        [
            FieldPanel('user_friendly_privacy_policy'),
        ],
        heading='Privacy policy',
        classname='collapsible'
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
        heading='Privacy policy links',
        classname='collapsible'
    ),
    MultiFieldPanel(
        [
            FieldPanel('meets_minimum_security_standards'),
            FieldPanel('show_ding_for_minimum_security_standards'),
            FieldPanel('uses_encryption'),
            FieldPanel('uses_encryption_helptext'),
            FieldPanel('security_updates'),
            FieldPanel('security_updates_helptext'),
            FieldPanel('strong_password'),
            FieldPanel('strong_password_helptext'),
            FieldPanel('manage_vulnerabilities'),
            FieldPanel('manage_vulnerabilities_helptext'),
            FieldPanel('privacy_policy'),
            FieldPanel('privacy_policy_helptext'),
        ],
        heading='Security',
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
    FieldPanel('updates'),
    RelatedProductFieldPanel('related_products'),
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

    # Privacy policy

    user_friendly_privacy_policy = ExtendedYesNoField(
        help_text='Does this product have a user-friendly privacy policy?'
    )

    # Minimum security standards

    meets_minimum_security_standards = models.BooleanField(
        null=True,
        help_text='Does this product meet our minimum security standards?',
    )

    show_ding_for_minimum_security_standards = models.BooleanField(
        default=False,
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

    def get_related_products(self):
        """
        This function is used by our custom RelatedProductFieldPanel, to make sure
        we don't list every single PNI product ever entered into the system, but only
        products added in recent iterations of PNI. For PNI v4 this has been set to
        "any product entered after 2019".
        """
        return Product.objects.filter(review_date__gte=date(2020, 1, 1)).order_by('name')

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
