from datetime import datetime

from django.conf import settings
from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.admin.edit_handlers import InlinePanel, FieldPanel, MultiFieldPanel, PageChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.core.models import Orderable, Page

from networkapi.buyersguide.fields import ExtendedYesNoField
from networkapi.buyersguide.pagemodels.cloudinary_image_field import (
    CloudinaryField
)
from networkapi.wagtailpages.pagemodels.mixin.foundation_metadata import (
    FoundationMetadataPageMixin
)
from networkapi.buyersguide.pagemodels.product_category import BuyersGuideProductCategory
from networkapi.buyersguide.pagemodels.product_update import Update

if settings.USE_CLOUDINARY:
    image_field = FieldPanel('cloudinary_image')
else:
    image_field = ImageChooserPanel('image')


class ProductPageCategory(Orderable):
    product = ParentalKey(
        'wagtailpages.ProductPage',
        related_name='product_categories',
        on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        'buyersguide.BuyersGuideProductCategory',
        related_name='+',
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
    )

    panels = [
        SnippetChooserPanel('category')
    ]

    def __str__(self):
        return self.category.name

    class Meta:
        verbose_name = "Product Category"


class RelatedProducts(Orderable):
    page = ParentalKey(
        'wagtailpages.ProductPage',
        related_name='related_product_pages',
        on_delete=models.CASCADE,
    )

    related_product = models.ForeignKey(
        'wagtailpages.ProductPage',
        on_delete=models.SET_NULL,
        null=True,
        related_name='+',
    )

    panels = [
        PageChooserPanel('related_product')
    ]


class ProductPagePrivacyPolicyLink(Orderable):
    page = ParentalKey(
        'wagtailpages.ProductPage',
        related_name='product_privacy_policy_links',
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

    panels = [
        FieldPanel('label'),
        FieldPanel('url'),
    ]

    def __str__(self):
        return f'{self.page.title}: {self.label} ({self.url})'


class ProductUpdates(Orderable):
    page = ParentalKey(
        'wagtailpages.ProductPage',
        related_name='product_updates',
        on_delete=models.CASCADE,
    )

    update = models.ForeignKey(
        Update,
        on_delete=models.SET_NULL,
        related_name='+',
        null=True,
    )

    panels = [
        SnippetChooserPanel('update')
    ]


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
        auto_now_add=True,
    )
    company = models.CharField(
        max_length=100,
        help_text='Name of Company',
        blank=True,
    )
    blurb = models.TextField(
        max_length=5000,
        help_text='Description of the product',
        blank=True
    )
    # TODO: We'll need to update this URL in the template
    product_url = models.URLField(
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

    """
    product_privacy_policy_links = Orderable, defined in ProductPagePrivacyPolicyLink
    Other "magic" relations that use InlinePanels will follow the same pattern of
    using Wagtail Orderables.
    """

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
        blank=True,
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

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel('privacy_ding'),
                FieldPanel('adult_content'),
                FieldPanel('company'),
                FieldPanel('product_url'),
                FieldPanel('price'),
                FieldPanel('uses_wifi'),
                FieldPanel('uses_bluetooth'),
                FieldPanel('blurb'),
                image_field,
                FieldPanel('worst_case'),
            ],
            heading='General Product Details',
            classname='collapsible'
        ),
        MultiFieldPanel(
            [
                InlinePanel('product_categories', label='Category'),
            ],
            heading='Product Categories',
            classname='collapsible',
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

                FieldPanel('how_does_it_use_data_collected'),
                FieldPanel('data_collection_policy_is_bad'),
            ],
            heading='How does it use this data',
            classname='collapsible',
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
                    'product_privacy_policy_links',
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
                FieldPanel('show_ding_for_minimum_security_standards'),
                FieldPanel('meets_minimum_security_standards'),
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
        MultiFieldPanel(
            [
                InlinePanel('product_updates', label='Update')
            ],
            heading='Product Updates',
        ),
        MultiFieldPanel(
            [
                InlinePanel('related_product_pages', label='Product')
            ],
            heading='Related Products',
        ),
    ]

    @property
    def is_current(self):
        d = self.review_date
        review = datetime(d.year, d.month, d.day)
        cutoff = datetime(2020, 10, 29)
        return cutoff < review

    class Meta:
        verbose_name = "Product Page"


class SoftwareProductPage(ProductPage):

    class Meta:
        verbose_name = "Software Product Page"


class GeneralProductPage(ProductPage):

    class Meta:
        verbose_name = "General Product Page"


class BuyersGuidePage(FoundationMetadataPageMixin, Page):
    template = 'buyersguide/home.html'
    subpage_types = [SoftwareProductPage, GeneralProductPage]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        if request.user.is_authenticated:
            products = ProductPage.objects.all()
        else:
            products = ProductPage.objects.live()

        # TODO:
        # Sort the products by their creepiness level. Example code below taken
        # from buyersguide/views.py
        # def get_average_creepiness(product_dict):
        #     try:
        #         votes = product_dict['votes']
        #         creepiness = votes['creepiness']
        #         avg = creepiness['average']
        #         return avg
        #     except TypeError:
        #         pass
        #     except AttributeError:
        #         pass

        #     return 50
        # products = cache.get_or_set(
        #     'sorted_product_dicts',
        #     lambda: sorted([p.to_dict() for p in Product.objects.all()], key=get_average_creepiness),
        #     86400
        # )

        context['categories'] = BuyersGuideProductCategory.objects.filter(hidden=False)
        context['products'] = products
        context['web_monetization_pointer'] = settings.WEB_MONETIZATION_POINTER
        return context

    class Meta:
        verbose_name = "Buyers Guide Page"
