import json

from datetime import datetime

from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.validators import int_list_validator
from django.db import Error, models
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseServerError, HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext, pgettext

from modelcluster.fields import ParentalKey

from wagtail.admin.edit_handlers import InlinePanel, FieldPanel, MultiFieldPanel, PageChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.models import Locale, Orderable, Page, TranslatableMixin

from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet

from wagtail_localize.fields import SynchronizedField, TranslatableField
from wagtail_airtable.mixins import AirtableMixin

from networkapi.wagtailpages.fields import ExtendedBoolean, ExtendedYesNoField
from networkapi.wagtailpages.pagemodels.mixin.foundation_metadata import (
    FoundationMetadataPageMixin
)
from networkapi.wagtailpages.templatetags.localization import relocalized_url
from networkapi.wagtailpages.utils import insert_panels_after, get_locale_from_request

# TODO: Move this util function
from networkapi.buyersguide.utils import get_category_og_image_upload_path
from .mixin.snippets import LocalizedSnippet
from networkapi.wagtailpages.utils import get_language_from_request

TRACK_RECORD_CHOICES = [
    ('Great', 'Great'),
    ('Average', 'Average'),
    ('Needs Improvement', 'Needs Improvement'),
    ('Bad', 'Bad')
]


def get_categories_for_locale(language_code):
    """
    Start with the English list of categories, and replace any of them
    with their localized counterpart, where possible, so that we don't
    end up with an incomplete category list due to missing locale records.
    """
    DEFAULT_LANGUAGE_CODE = settings.LANGUAGE_CODE
    DEFAULT_LOCALE = Locale.objects.get(language_code=DEFAULT_LANGUAGE_CODE)

    default_locale_list = BuyersGuideProductCategory.objects.filter(
        hidden=False,
        locale=DEFAULT_LOCALE,
    )

    if language_code == DEFAULT_LANGUAGE_CODE:
        return default_locale_list

    try:
        actual_locale = Locale.objects.get(language_code=language_code)
    except Locale.DoesNotExist:
        actual_locale = Locale.objects.get(language_code=settings.LANGUAGE_CODE)

    return [
        BuyersGuideProductCategory.objects.filter(
            translation_key=cat.translation_key,
            locale=actual_locale,
        ).first() or cat for cat in default_locale_list
    ]


def get_product_subset(cutoff_date, authenticated, key, products, language_code='en'):
    """
    filter a queryset based on our current cutoff date,
    as well as based on whether a user is authenticated
    to the system or not (authenticated users get to
    see all products, including draft products)
    """
    try:
        locale = Locale.objects.get(language_code=language_code)
    except Locale.DoesNotExist:
        locale = Locale.objects.get(language_code=settings.LANGUAGE_CODE)

    products = products.filter(review_date__gte=cutoff_date, locale=locale)

    if not authenticated:
        products = products.live()

    products = sort_average(products)
    return cache.get_or_set(key, products, 86400)


def sort_average(products):
    """
    `products` is a QuerySet of ProductPages.
    """
    return sorted(products, key=lambda p: p.creepiness)


@register_snippet
class BuyersGuideProductCategory(TranslatableMixin, LocalizedSnippet, models.Model):
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
        help_text='A URL-friendly version of the category name. This is an auto-generated field.'
    )

    sort_order = models.IntegerField(
        default=1,
        help_text='Sort ordering number. Same-numbered items sort alphabetically'
    )

    og_image = models.FileField(
        max_length=2048,
        help_text='Image to use as OG image',
        upload_to=get_category_og_image_upload_path,
        blank=True,
    )

    translatable_fields = [
        TranslatableField('name'),
        TranslatableField('description'),
        SynchronizedField('slug'),
    ]

    @property
    def published_product_page_count(self):
        return ProductPage.objects.filter(product_categories__category=self).live().count()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta(TranslatableMixin.Meta):
        verbose_name = "Buyers Guide Product Category"
        verbose_name_plural = "Buyers Guide Product Categories"
        ordering = ['sort_order', 'name', ]


class ProductPageVotes(models.Model):
    """
    PNI product voting bins. This does not need translating.
    """
    vote_bins = models.CharField(default="0,0,0,0,0", max_length=50, validators=[int_list_validator])

    def set_votes(self, bin_list):
        """
        There are 5 "bins" for votes: <20%, <40%, <60%, <80%, <100%.
        When setting votes, ensure there are only 5 bins (max)
        """
        bin_list = [str(x) for x in bin_list]
        self.vote_bins = ','.join(bin_list[0:5])
        self.save()

    def get_votes(self):
        """Pull the votes out of the database and split them. Convert to ints."""
        votes = [int(x) for x in self.vote_bins.split(",")]
        return votes


class ProductPageCategory(TranslatableMixin, Orderable):
    product = ParentalKey(
        'wagtailpages.ProductPage',
        related_name='product_categories',
        on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        'wagtailpages.BuyersGuideProductCategory',
        related_name='+',
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
    )
    panels = [
        SnippetChooserPanel('category'),
    ]

    def __str__(self):
        return self.category.name

    class Meta(TranslatableMixin.Meta):
        verbose_name = "Product Category"


class RelatedProducts(TranslatableMixin, Orderable):
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

    class Meta(TranslatableMixin.Meta):
        verbose_name = 'Related Product'


class ProductPagePrivacyPolicyLink(TranslatableMixin, Orderable):
    page = ParentalKey(
        'wagtailpages.ProductPage',
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

    panels = [
        FieldPanel('label'),
        FieldPanel('url'),
    ]

    translatable_fields = [
        TranslatableField('label'),
        SynchronizedField('url'),
    ]

    def __str__(self):
        return f'{self.page.title}: {self.label} ({self.url})'

    class Meta(TranslatableMixin.Meta):
        verbose_name = 'Privacy Link'


@register_snippet
class Update(TranslatableMixin, index.Indexed, models.Model):
    source = models.URLField(
        max_length=2048,
        help_text='Link to source',
    )

    title = models.CharField(
        max_length=256,
    )

    author = models.CharField(
        max_length=256,
        blank=True,
    )

    featured = models.BooleanField(
        default=False,
        help_text='feature this update at the top of the list?'
    )

    snippet = models.TextField(
        max_length=5000,
        blank=True,
    )

    created_date = models.DateField(
        auto_now_add=True,
        help_text='The date this product was created',
    )

    panels = [
        FieldPanel('source'),
        FieldPanel('title'),
        FieldPanel('author'),
        FieldPanel('featured'),
        FieldPanel('snippet'),
    ]

    search_fields = [
        index.SearchField('title', partial_match=True),
    ]

    translatable_fields = [
        SynchronizedField('source'),
        SynchronizedField('title'),
        SynchronizedField('author'),
        SynchronizedField('snippet'),
    ]

    def __str__(self):
        return self.title

    class Meta(TranslatableMixin.Meta):
        verbose_name = "Buyers Guide Product Update"
        verbose_name_plural = "Buyers Guide Product Updates"


class ProductUpdates(TranslatableMixin, Orderable):
    page = ParentalKey(
        'wagtailpages.ProductPage',
        related_name='updates',
        on_delete=models.CASCADE,
    )

    # This is the new update FK to wagtailpages.Update
    update = models.ForeignKey(
        Update,
        on_delete=models.SET_NULL,
        related_name='+',
        null=True
    )

    translatable_fields = [
        TranslatableField("update"),
    ]

    panels = [
        SnippetChooserPanel('update'),
    ]

    class Meta(TranslatableMixin.Meta):
        verbose_name = 'Product Update'


class ProductPage(AirtableMixin, FoundationMetadataPageMixin, Page):
    """
    ProductPage is the superclass that SoftwareProductPage and
    GeneralProductPage inherit from. This should not be an abstract
    model as we need it to connect the two page types together.
    """

    template = 'buyersguide/product_page.html'

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
        default=timezone.now,
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
    worst_case = models.TextField(
        max_length=5000,
        help_text="What's the worst thing that could happen by using this product?",
        blank=True,
    )

    """
    privacy_policy_links = Orderable, defined in ProductPagePrivacyPolicyLink
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

    user_friendly_privacy_policy_helptext = models.TextField(
        max_length=5000,
        blank=True
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

    # Un-editable voting fields. Don't add these to the content_panels.
    creepiness_value = models.IntegerField(default=0)  # The total points for creepiness
    votes = models.ForeignKey(
        ProductPageVotes,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='votes',
    )

    @classmethod
    def map_import_fields(cls):
        mappings = {
            "Title": "title",
            "Wagtail Page ID": "pk",
            "Slug": "slug",
            "Show privacy ding": "privacy_ding",
            "Has adult content": "adult_content",
            "Uses wifi": "uses_wifi",
            "Uses Bluetooth": "uses_bluetooth",
            "Review date": "review_date",
            "Company": "company",
            "Blurb": "blurb",
            "Product link": "product_url",
            "Price": "price",
            "Worst case": "worst_case",
            "Signup requires email": "signup_requires_email",
            "Signup requires phone number": "signup_requires_phone",
            "Signup requires 3rd party account": "signup_requires_third_party_account",
            "Signup explanation": "signup_requirement_explanation",
            "How it collects data": "how_does_it_use_data_collected",
            "Data collection privacy ding": "data_collection_policy_is_bad",
            "User friendly privacy policy": "user_friendly_privacy_policy",
            "User friendly privacy policy help text": "user_friendly_privacy_policy_helptext",
            "Meets MSS": "meets_minimum_security_standards",
            "Meets MSS privacy policy ding": "show_ding_for_minimum_security_standards",
            "Uses encryption": "uses_encryption",
            "Encryption help text": "uses_encryption_helptext",
            "Has security updates": "security_updates",
            "Security updates help text": "security_updates_helptext",
            "Strong password": "strong_password",
            "Strong password help text": "strong_password_helptext",
            "Manages security vulnerabilities": "manage_vulnerabilities",
            "Manages security help text": "manage_vulnerabilities_helptext",
            "Has privacy policy": "privacy_policy",
            "Privacy policy help text": "privacy_policy_helptext",
            "Phone number": "phone_number",
            "Live chat": "live_chat",
            "Email address": "email",
            "Twitter": "twitter",
        }
        return mappings

    def get_export_fields(self):
        """
        This should be a dictionary of the fields to send to Airtable.
        Keys are the Column Names in Airtable. Values are the Wagtail values we want to send.
        """
        return {
            "Title": self.title,
            "Slug": self.slug,
            "Wagtail Page ID": self.pk if hasattr(self, 'pk') else 0,
            "Last Updated": str(self.last_published_at) if self.last_published_at else str(timezone.now().isoformat()),
            "Status": self.get_status_for_airtable(),
            "Show privacy ding": self.privacy_ding,
            "Has adult content": self.adult_content,
            "Uses wifi": self.uses_wifi,
            "Uses Bluetooth": self.uses_bluetooth,
            "Review date": str(self.review_date),
            "Company": self.company,
            "Blurb": self.blurb,
            "Product link": self.product_url if self.product_url else '',
            "Price": self.price,
            "Worst case": self.worst_case,
            "Signup requires email": self.signup_requires_email,
            "Signup requires phone number": self.signup_requires_phone,
            "Signup requires 3rd party account": self.signup_requires_third_party_account,
            "Signup explanation": self.signup_requirement_explanation,
            "How it collects data": self.how_does_it_use_data_collected,
            "Data collection privacy ding": self.data_collection_policy_is_bad,
            "User friendly privacy policy": self.user_friendly_privacy_policy,
            "User friendly privacy policy help text": self.user_friendly_privacy_policy_helptext,
            "Meets MSS": self.meets_minimum_security_standards,
            "Meets MSS privacy policy ding": self.show_ding_for_minimum_security_standards,
            "Uses encryption": self.uses_encryption,
            "Encryption help text": self.uses_encryption_helptext,
            "Has security updates": self.security_updates,
            "Security updates help text": self.security_updates_helptext,
            "Strong password": self.strong_password,
            "Strong password help text": self.strong_password_helptext,
            "Manages security vulnerabilities": self.manage_vulnerabilities,
            "Manages security help text": self.manage_vulnerabilities_helptext,
            "Has privacy policy": self.privacy_policy,
            "Privacy policy help text": self.privacy_policy_helptext,
            "Phone number": self.phone_number,
            "Live chat": self.live_chat,
            "Email address": self.email,
            "Twitter": self.twitter if self.twitter else ''
        }

    def get_status_for_airtable(self):
        if self.live:
            if self.has_unpublished_changes:
                return "Live + Draft"
            return "Live"
        return "Draft"

    @property
    def total_vote_count(self):
        return sum(self.get_or_create_votes())

    @property
    def creepiness(self):
        try:
            average = self.creepiness_value / self.total_vote_count
        except ZeroDivisionError:
            average = 50
        return average

    @property
    def get_voting_json(self):
        """
        Return a dictionary as a string with the relevant data needed for the frontend:
        """
        votes = self.votes.get_votes()
        data = {
            'creepiness': {
                'vote_breakdown':  {k: v for (k, v) in enumerate(votes)},
                'average': self.creepiness
            },
            'total': self.total_vote_count
        }
        return json.dumps(data)

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel('review_date'),
                FieldPanel('privacy_ding'),
                FieldPanel('adult_content'),
                FieldPanel('company'),
                FieldPanel('product_url'),
                FieldPanel('price'),
                FieldPanel('uses_wifi'),
                FieldPanel('uses_bluetooth'),
                FieldPanel('blurb'),
                ImageChooserPanel('image'),
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
                FieldPanel('user_friendly_privacy_policy_helptext'),
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
                InlinePanel('updates', label='Update')
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

    translatable_fields = [
        # Promote tab fields
        SynchronizedField('slug'),
        TranslatableField('seo_title'),
        SynchronizedField('show_in_menus'),
        TranslatableField('search_description'),
        SynchronizedField('search_image'),
        # Content tab fields
        TranslatableField('title'),
        TranslatableField('search_description'),
        SynchronizedField('privacy_ding'),
        SynchronizedField('adult_content'),
        SynchronizedField('uses_wifi'),
        SynchronizedField('uses_bluetooth'),
        SynchronizedField('review_date'),
        SynchronizedField('company'),
        TranslatableField('blurb'),
        SynchronizedField('product_url'),
        TranslatableField('price'),
        SynchronizedField('image'),
        TranslatableField('worst_case'),
        SynchronizedField('signup_requires_email'),
        SynchronizedField('signup_requires_phone'),
        SynchronizedField('signup_requires_third_party_account'),
        TranslatableField('signup_requirement_explanation'),
        SynchronizedField('signup_requires_third_party_account'),
        TranslatableField('how_does_it_use_data_collected'),
        SynchronizedField('data_collection_policy_is_bad'),
        SynchronizedField('user_friendly_privacy_policy'),
        TranslatableField('user_friendly_privacy_policy_helptext'),
        SynchronizedField('show_ding_for_minimum_security_standards'),
        SynchronizedField('meets_minimum_security_standards'),
        SynchronizedField('uses_encryption'),
        TranslatableField('uses_encryption_helptext'),
        SynchronizedField('security_updates'),
        TranslatableField('security_updates_helptext'),
        SynchronizedField('strong_password'),
        TranslatableField('strong_password_helptext'),
        SynchronizedField('manage_vulnerabilities'),
        TranslatableField('manage_vulnerabilities_helptext'),
        SynchronizedField('privacy_policy'),
        TranslatableField('privacy_policy_helptext'),
        SynchronizedField('phone_number'),
        SynchronizedField('live_chat'),
        SynchronizedField('email'),
        SynchronizedField('twitter'),
    ]

    @property
    def product_type(self):
        return "unknown"

    def get_or_create_votes(self):
        """
        If a page doesn't have a ProductPageVotes objects, create it.
        Regardless of whether or not its created, return the parsed votes.
        """
        if not self.votes:
            votes = ProductPageVotes()
            votes.save()
            self.votes = votes
            self.save()
        return self.votes.get_votes()

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['product'] = self
        language_code = get_language_from_request(request)
        context['categories'] = get_categories_for_locale(language_code)
        context['mediaUrl'] = settings.MEDIA_URL
        context['use_commento'] = settings.USE_COMMENTO
        context['pageTitle'] = f'{self.title} | ' + gettext("Privacy & security guide") + ' | Mozilla Foundation'
        pni_home_page = BuyersGuidePage.objects.first()
        context['about_page'] = pni_home_page
        context['home_page'] = pni_home_page
        return context

    def serve(self, request, *args, **kwargs):
        # In Wagtail we use the serve() method to detect POST submissions.
        # Alternatively, this could be a routable view.
        # For more on this, see the docs here:
        # https://docs.wagtail.io/en/stable/reference/pages/model_recipes.html#overriding-the-serve-method
        if request.body and request.method == "POST":
            # If the request is POST. Parse the body.
            data = json.loads(request.body)
            # If the POST body has a productID and value, it's someone voting on the product
            if data.get("value"):
                # Product ID and Value can both be zero. It's impossible to get a Page with ID of zero.
                try:
                    value = int(data["value"])  # ie. 0 to 100
                except ValueError:
                    return HttpResponseNotAllowed('Product ID or value is invalid')

                if value < 0 or value > 100:
                    return HttpResponseNotAllowed('Cannot save vote')

                try:
                    product = ProductPage.objects.get(pk=self.id)
                    # If the product exists but isn't live and the user isn't logged in..
                    if (not product.live and not request.user.is_authenticated) or not product:
                        return HttpResponseNotFound("Product does not exist")

                    # Save the new voting totals
                    product.creepiness_value = product.creepiness_value + value

                    # Add the vote to the vote bin
                    if not product.votes:
                        # If there is no vote bin attached to this product yet, create one now.
                        votes = ProductPageVotes()
                        votes.save()
                        product.votes = votes

                    # Add the vote to the proper "vote bin"
                    votes = product.votes.get_votes()
                    index = int((value-1) / 20)
                    votes[index] += 1
                    product.votes.set_votes(votes)

                    # Don't save this as a revision with .save_revision() as to not spam the Audit log
                    # And don't make this live with .publish(). The Page model will have the proper
                    # data stored on it already, and the revision history won't be spammed by votes.
                    product.save()
                    return HttpResponse('Vote recorded', content_type='text/plain')
                except ProductPage.DoesNotExist:
                    return HttpResponseNotFound('Missing page')
                except ValidationError as ex:
                    return HttpResponseNotAllowed(f'Payload validation failed: {ex}')
                except Error as ex:
                    print(f'Internal Server Error (500) for ProductPage: {ex.message} ({type(ex)})')
                    return HttpResponseServerError()

        self.get_or_create_votes()

        return super().serve(request, *args, **kwargs)

    def save(self, *args, **kwargs):
        # When a new ProductPage is created, ensure a vote bin always exists.
        # We can use save() or a post-save Wagtail hook.
        save = super().save(*args, **kwargs)
        self.get_or_create_votes()
        return save

    class Meta:
        verbose_name = "Product Page"


class SoftwareProductPage(ProductPage):
    template = 'buyersguide/product_page.html'

    handles_recordings_how = models.TextField(
        max_length=5000,
        blank=True,
        help_text='How does this software handle your recordings'
    )

    recording_alert = ExtendedYesNoField(
        null=True,
        help_text='Alerts when calls are being recorded?',
    )

    recording_alert_helptext = models.TextField(
        max_length=5000,
        blank=True
    )

    medical_privacy_compliant = ExtendedBoolean(
        help_text='Compliant with US medical privacy laws?'
    )

    medical_privacy_compliant_helptext = models.TextField(
        max_length=5000,
        blank=True
    )

    # Can I control it?

    host_controls = models.TextField(
        max_length=5000,
        blank=True
    )

    easy_to_learn_and_use = ExtendedBoolean(
        help_text='Is it easy to learn & use the features?',
    )

    easy_to_learn_and_use_helptext = models.TextField(
        max_length=5000,
        blank=True
    )

    @classmethod
    def map_import_fields(cls):
        generic_product_import_fields = super().map_import_fields()
        software_product_mappings = {
            "How it handles recording": "handles_recordings_how",
            "Recording alert": "recording_alert",
            "Recording alert help text": "recording_alert_helptext",
            "Medical privacy compliant": "medical_privacy_compliant",
            "Medical privacy compliant help text": "medical_privacy_compliant_helptext",
            "Host controls": "host_controls",
            "Easy to learn and use": "easy_to_learn_and_use",
            "Easy to learn and use help text": "easy_to_learn_and_use_helptext",
        }
        # Return the merged fields
        return {**generic_product_import_fields, **software_product_mappings}

    def get_export_fields(self):
        """
        This should be a dictionary of the fields to send to Airtable.
        Keys are the Column Names in Airtable. Values are the Wagtail values we want to send.
        """
        generic_product_data = super().get_export_fields()
        software_product_data = {
            "How it handles recording": self.handles_recordings_how,
            "Recording alert": self.recording_alert,
            "Recording alert help text": self.recording_alert_helptext,
            "Medical privacy compliant": True if self.medical_privacy_compliant else False,
            "Medical privacy compliant help text": self.medical_privacy_compliant_helptext,
            "Host controls": self.host_controls,
            "Easy to learn and use": True if self.easy_to_learn_and_use else False,
            "Easy to learn and use help text": self.easy_to_learn_and_use_helptext,
        }

        data = {**generic_product_data, **software_product_data}
        return data

    content_panels = ProductPage.content_panels.copy()
    content_panels = insert_panels_after(
        content_panels,
        'Product Categories',
        [
            MultiFieldPanel(
                [
                    FieldPanel('handles_recordings_how'),
                    FieldPanel('recording_alert'),
                    FieldPanel('recording_alert_helptext'),
                    FieldPanel('medical_privacy_compliant'),
                    FieldPanel('medical_privacy_compliant_helptext'),
                ],
                heading='How does it handle privacy?',
                classname='collapsible'
            ),
            MultiFieldPanel(
                [
                    FieldPanel('host_controls'),
                    FieldPanel('easy_to_learn_and_use'),
                    FieldPanel('easy_to_learn_and_use_helptext'),
                ],
                heading='Can I control it',
                classname='collapsible'
            ),
        ],
    )

    translatable_fields = ProductPage.translatable_fields + [
        TranslatableField('handles_recordings_how'),
        SynchronizedField('recording_alert'),
        TranslatableField('recording_alert_helptext'),
        SynchronizedField('medical_privacy_compliant'),
        TranslatableField('medical_privacy_compliant_helptext'),
        TranslatableField('host_controls'),
        SynchronizedField('easy_to_learn_and_use'),
        TranslatableField('easy_to_learn_and_use_helptext'),
    ]

    @property
    def product_type(self):
        return "software"

    # TODO: Needs translatable_fields
    class Meta:
        verbose_name = "Software Product Page"


class GeneralProductPage(ProductPage):
    template = 'buyersguide/product_page.html'

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

    # How can you control your data

    how_can_you_control_your_data = models.TextField(
        max_length=5000,
        blank=True,
        help_text='How does this product let you control your data?'
    )

    data_control_policy_is_bad = models.BooleanField(
        default=False,
        verbose_name='Privacy ding'
    )

    # Company track record

    company_track_record = models.CharField(
        choices=TRACK_RECORD_CHOICES,
        default='Average',
        help_text='This company has a ... track record',
        max_length=20
    )

    track_record_is_bad = models.BooleanField(
        default=False,
        verbose_name='Privacy ding'
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
        help_text='Does the product use AI?'
    )

    ai_uses_personal_data = ExtendedYesNoField(
        help_text='Does the AI use your personal data to make decisions about you?'
    )

    ai_is_transparent = ExtendedYesNoField(
        help_text='Does the company allow users to see how the AI works?'
    )

    ai_helptext = models.TextField(
        max_length=5000,
        blank=True,
        help_text='Helpful text around AI to show on the product page',
    )

    @classmethod
    def map_import_fields(cls):
        generic_product_import_fields = super().map_import_fields()
        general_product_mappings = {
            "Has camera device": "camera_device",
            "Has camera app": "camera_app",
            "Has microphone device": "microphone_device",
            "Has microphone app": "microphone_app",
            "Has location device": "location_device",
            "Has location app": "location_app",
            "Personal data collected": "personal_data_collected",
            "Biometric data collected": "biometric_data_collected",
            "Social data collected": "social_data_collected",
            "How you can control your data": "how_can_you_control_your_data",
            "Company track record": "company_track_record",
            "Show company track record privacy ding": "track_record_is_bad",
            "Offline capable": "offline_capable",
            "Offline use": "offline_use_description",
            "Uses AI": "uses_ai",
            "AI uses personal data": "ai_uses_personal_data",
            "AI help text": "ai_helptext",
            "AI is transparent": "ai_is_transparent",
        }
        # Return the merged fields
        return {**generic_product_import_fields, **general_product_mappings}

    def get_export_fields(self):
        """
        This should be a dictionary of the fields to send to Airtable.
        Keys are the Column Names in Airtable. Values are the Wagtail values we want to send.
        """
        generic_product_data = super().get_export_fields()
        general_product_data = {
            "Has camera device": self.camera_device,
            "Has camera app": self.camera_app,
            "Has microphone device": self.microphone_device,
            "Has microphone app": self.microphone_app,
            "Has location device": self.location_device,
            "Has location app": self.location_app,
            "Personal data collected": self.personal_data_collected,
            "Biometric data collected": self.biometric_data_collected,
            "Social data collected": self.social_data_collected,
            "How you can control your data": self.how_can_you_control_your_data,
            "Company track record": self.company_track_record,
            "Show company track record privacy ding": self.track_record_is_bad,
            "Offline capable": self.offline_capable,
            "Offline use": self.offline_use_description,
            "Uses AI": self.uses_ai,
            "AI uses personal data": self.ai_uses_personal_data,
            "AI is transparent": self.ai_uses_personal_data,
            "AI help text": self.ai_helptext,
        }
        # Merge the two dicts together.
        data = {**generic_product_data, **general_product_data}
        return data

    # administrative panels
    content_panels = ProductPage.content_panels.copy()
    content_panels = insert_panels_after(
        content_panels,
        'Product Categories',
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

    content_panels = insert_panels_after(
        content_panels,
        'What is required to sign up',
        [
            MultiFieldPanel(
                [
                    FieldPanel('personal_data_collected'),
                    FieldPanel('biometric_data_collected'),
                    FieldPanel('social_data_collected'),
                ],
                heading='What data does it collect',
                classname='collapsible',
            ),
        ]
    )

    content_panels = insert_panels_after(
        content_panels,
        'How does it use this data',
        [
            MultiFieldPanel(
                [
                    FieldPanel('how_can_you_control_your_data'),
                    FieldPanel('data_control_policy_is_bad'),
                ],
                heading='How can you control your data',
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

    content_panels = insert_panels_after(
        content_panels,
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
        ],
    )

    translatable_fields = ProductPage.translatable_fields + [
        TranslatableField('personal_data_collected'),
        TranslatableField('biometric_data_collected'),
        TranslatableField('social_data_collected'),
        TranslatableField('how_can_you_control_your_data'),
        SynchronizedField('data_control_policy_is_bad'),
        SynchronizedField('company_track_record'),
        SynchronizedField('track_record_is_bad'),
        TranslatableField('track_record_details'),
        SynchronizedField('offline_capable'),
        TranslatableField('offline_use_description'),
        SynchronizedField('uses_ai'),
        SynchronizedField('ai_uses_personal_data'),
        SynchronizedField('ai_is_transparent'),
        TranslatableField('ai_helptext'),
    ]

    @property
    def product_type(self):
        return "general"

    class Meta:
        verbose_name = "General Product Page"


class ExcludedCategories(TranslatableMixin, Orderable):
    """
    This allows us to filter categories from showing up on the PNI site
    """

    page = ParentalKey("wagtailpages.BuyersGuidePage", related_name="excluded_categories")
    category = models.ForeignKey(
        BuyersGuideProductCategory,
        on_delete=models.CASCADE,
    )

    panels = [
        SnippetChooserPanel("category"),
    ]

    def __str__(self):
        return self.category.name

    class Meta(TranslatableMixin.Meta):
        verbose_name = 'Excluded Category'


class BuyersGuidePage(RoutablePageMixin, FoundationMetadataPageMixin, Page):
    """
    Note: We'll likely be converting the "about" pages to Wagtail Pages.
    When that happens, we should remove the RoutablePageMixin and @routes
    """

    template = 'buyersguide/home.html'
    subpage_types = [SoftwareProductPage, GeneralProductPage]

    cutoff_date = models.DateField(
        'Product listing cutoff date',
        help_text='Only show products that were reviewed on, or after this date.',
        default=datetime(2020, 10, 29),
    )

    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='pni_hero_image'
    )

    header = models.CharField(
        max_length=120,
        blank=True,
        help_text='The header text for the PNI homepage',
    )

    intro_text = models.TextField(
        max_length=500,
        blank=True,
        help_text='A short blurb to show under the header',
    )

    dark_theme = models.BooleanField(
        default=False,
        help_text='Does the intro need to be white text (for dark backgrounds)?'
    )

    def get_banner(self):
        return self.hero_image

    content_panels = [
        FieldPanel('title'),
        FieldPanel('cutoff_date'),
        ImageChooserPanel('hero_image'),
        FieldPanel('header'),
        FieldPanel('intro_text'),
        FieldPanel('dark_theme'),
        MultiFieldPanel(
            [
                InlinePanel("excluded_categories", label="Category", min_num=0)
            ],
            heading="Excluded Categories"
        ),
    ]

    translatable_fields = [
        TranslatableField('title'),
        SynchronizedField('hero_image'),
        TranslatableField('header'),
        TranslatableField('intro_text'),
        SynchronizedField('dark_theme'),
        # Promote tab fields
        TranslatableField('seo_title'),
        TranslatableField('search_description'),
        SynchronizedField('search_image'),
    ]

    @route(r'^about/$', name='how-to-use-view')
    def about_page(self, request):
        context = self.get_context(request)
        context['pagetype'] = 'about'
        context['pageTitle'] = pgettext(
            '*privacy not included can be localized.',
            'How to use *privacy not included')
        return render(request, "about/how_to_use.html", context)

    @route(r'^about/why/$', name='about-why-view')
    def about_why_page(self, request):
        context = self.get_context(request)
        context['pagetype'] = 'about'
        context['pageTitle'] = pgettext(
            '*privacy not included can be localized.',
            'Why we made *privacy not included')
        return render(request, "about/why_we_made.html", context)

    @route(r'^about/press/$', name='press-view')
    def about_press_page(self, request):
        context = self.get_context(request)
        context['pagetype'] = 'about'
        context['pageTitle'] = pgettext('Noun, media', 'Press') + ' | ' + pgettext(
            'This can be localized. This is a reference to the “*batteries not included” mention on toys.',
            '*privacy not included')
        return render(request, "about/press.html", context)

    @route(r'^about/contact/$', name='contact-view')
    def about_contact_page(self, request):
        context = self.get_context(request)
        context['pagetype'] = 'about'
        context['pageTitle'] = gettext('Contact us') + ' | ' + pgettext(
            'This can be localized. This is a reference to the “*batteries not included” mention on toys.',
            '*privacy not included')
        return render(request, "about/contact.html", context)

    @route(r'^about/methodology/$', name='methodology-view')
    def about_methodology_page(self, request):
        context = self.get_context(request)
        context['pagetype'] = 'about'
        context['pageTitle'] = gettext('Our methodology') + ' | ' + pgettext(
            'This can be localized. This is a reference to the “*batteries not included” mention on toys.',
            '*privacy not included')
        return render(request, "about/methodology.html", context)

    @route(r'^about/meets-minimum-security-standards/$', name='min-security-view')
    def about_mss_page(self, request):
        context = self.get_context(request)
        context['pagetype'] = 'about'
        context['pageTitle'] = gettext('Our minimum security standards') + ' | ' + pgettext(
            'This can be localized. This is a reference to the “*batteries not included” mention on toys.',
            '*privacy not included')
        return render(request, "about/minimum_security.html", context)

    @route(r'^contest/$', name='contest')
    def about_contest(self, request):
        context = self.get_context(request)
        context['pagetype'] = 'contest'
        context['pageTitle'] = gettext('Contest terms and conditions') + ' | ' + pgettext(
            'This can be localized. This is a reference to the “*batteries not included” mention on toys.',
            '*privacy not included')
        return render(request, "buyersguide/contest.html", context)

    @route(r'^products/(?P<slug>[-\w\d]+)/$', name='product-view')
    def product_view(self, request, slug):
        # Find product by it's slug and redirect to the product page
        # If no product is found, redirect to the BuyersGuide page
        locale = get_locale_from_request(request)
        product = get_object_or_404(ProductPage, slug=slug, locale=locale)
        url = relocalized_url(product.url, locale.language_code)
        return redirect(url)

    @route(r'^categories/(?P<slug>[\w\W]+)/', name='category-view')
    def categories_page(self, request, slug):
        context = self.get_context(request, bypass_products=True)
        language_code = get_language_from_request(request)
        locale_id = Locale.objects.get(language_code=language_code).id
        slug = slugify(slug)

        DEFAULT_LOCALE = Locale.objects.get(language_code=settings.LANGUAGE_CODE)
        DEFAULT_LOCALE_ID = DEFAULT_LOCALE.id

        # because we may be working with localized content, and the slug
        # will always be our english slug, we need to find the english
        # category first, and then find its corresponding localized version
        try:
            original_category = BuyersGuideProductCategory.objects.get(slug=slug, locale_id=DEFAULT_LOCALE_ID)
        except BuyersGuideProductCategory.DoesNotExist:
            original_category = get_object_or_404(BuyersGuideProductCategory, name__iexact=slug)

        if locale_id != DEFAULT_LOCALE_ID:
            try:
                category = BuyersGuideProductCategory.objects.get(
                    translation_key=original_category.translation_key,
                    locale_id=DEFAULT_LOCALE_ID,
                )
            except BuyersGuideProductCategory.DoesNotExist:
                category = original_category
        else:
            category = original_category

        authenticated = request.user.is_authenticated
        key = f'cat_product_dicts_{slug}_auth' if authenticated else f'cat_product_dicts_{slug}_live'
        key = f'{language_code}_{key}'
        products = cache.get(key)
        exclude_cat_ids = [excats.category.id for excats in self.excluded_categories.all()]

        if products is None:
            products = get_product_subset(
                self.cutoff_date,
                authenticated,
                key,
                ProductPage.objects.filter(product_categories__category__in=[original_category])
                                   .exclude(product_categories__category__id__in=exclude_cat_ids),
                language_code=language_code
            )

        context['category'] = slug
        context['current_category'] = category
        context['products'] = products
        context['pageTitle'] = f'{category} | ' + gettext("Privacy & security guide") + ' | Mozilla Foundation'
        context['template_cache_key_fragment'] = f'{category.slug}_{request.LANGUAGE_CODE}'

        return render(request, "buyersguide/category_page.html", context)

    def get_sitemap_urls(self, request):
        """
        Add categories and route views to the sitemap for better search indexing.
        """
        sitemap = super().get_sitemap_urls(request)
        last_modified = self.last_published_at or self.latest_revision_created_at
        # Add all the available Buyers Guide categories to the sitemap
        categories = BuyersGuideProductCategory.objects.filter(hidden=False)
        for category in categories:
            sitemap.append(
                {
                    "location": self.full_url + self.reverse_subpage("category-view", args=(category.slug,)),
                    "lastmod": last_modified,
                }
            )

        # Add all the available "subpages" (routes) to the sitemap, excluding categories and products.
        # Categories are added above. Products will be their own Wagtail pages and get their own URLs because of that.
        about_page_views = [
            'how-to-use-view', 'about-why-view', 'press-view',
            'contact-view', 'methodology-view', 'min-security-view'
        ]
        for about_page in about_page_views:
            sitemap.append(
                {
                    "location": self.full_url + self.reverse_subpage(about_page),
                    "lastmod": last_modified,
                }
            )
        return sitemap

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        language_code = get_language_from_request(request)

        authenticated = request.user.is_authenticated
        key = 'home_product_dicts_authed' if authenticated else 'home_product_dicts_live'
        key = f'{key}_{language_code}'
        products = cache.get(key)
        exclude_cat_ids = [excats.category.id for excats in self.excluded_categories.all()]

        if not kwargs.get('bypass_products', False) and products is None:
            products = get_product_subset(
                self.cutoff_date,
                authenticated,
                key,
                ProductPage.objects.exclude(product_categories__category__id__in=exclude_cat_ids),
                language_code=language_code
            )

        context['categories'] = get_categories_for_locale(language_code)
        context['products'] = products
        context['web_monetization_pointer'] = settings.WEB_MONETIZATION_POINTER
        pni_home_page = BuyersGuidePage.objects.first()
        context['about_page'] = pni_home_page
        context['home_page'] = pni_home_page
        context['template_cache_key_fragment'] = f'pni_home_{request.LANGUAGE_CODE}'
        return context

    class Meta:
        verbose_name = "Buyers Guide Page"


def get_pni_home_page():
    """
    Used in AIRTABLE settings for nesting child pages under a new parent page.
    """
    return BuyersGuidePage.objects.first().id
