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
from django.utils.translation import pgettext

from modelcluster.fields import ParentalKey

from wagtail.admin.edit_handlers import InlinePanel, FieldPanel, MultiFieldPanel, PageChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
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
from networkapi.buyersguide.throttle import UserVoteRateThrottle, TestUserVoteRateThrottle
from networkapi.wagtailpages.utils import insert_panels_after


if settings.USE_CLOUDINARY:
    image_field = FieldPanel('cloudinary_image')
    MEDIA_URL = settings.CLOUDINARY_URL
else:
    image_field = ImageChooserPanel('image')
    MEDIA_URL = settings.MEDIA_URL

vote_throttle_class = UserVoteRateThrottle if not settings.TESTING else TestUserVoteRateThrottle


def sort_average(products):
    """
    `products` is a QuerySet of ProductPages.
    """
    return sorted(products, key=lambda p: p.creepiness)


class ProductPageVotes(models.Model):
    vote_bin = models.CharField(default="0,0,0,0,0", max_length=50, validators=[int_list_validator])

    def set_votes(self, bin_list):
        """
        There are 5 "bins" for votes: <20%, <40%, <60%, <80%, <100%.
        When setting votes, ensure there are only 5 bins (max)
        """
        bin_list = [str(x) for x in bin_list]
        self.vote_bin = ','.join(bin_list[0:5])
        self.save()

    def get_votes(self):
        """Pull the votes out of the database and split them. Convert to ints."""
        votes = [int(x) for x in self.vote_bin.split(",")]
        return votes


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

    def __str__(self):
        return f'{self.page.title}: {self.label} ({self.url})'


class ProductUpdates(Orderable):
    page = ParentalKey(
        'wagtailpages.ProductPage',
        related_name='updates',
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
        default=timezone.now
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

    @property
    def is_current(self):
        d = self.review_date
        review = datetime(d.year, d.month, d.day)
        cutoff = datetime(2020, 10, 29)
        return cutoff < review

    @property
    def product_type(self):
        if isinstance(self, SoftwareProductPage):
            return "software"
        elif isinstance(self, GeneralProductPage):
            return "general"
        else:
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
        context['categories'] = BuyersGuideProductCategory.objects.filter(hidden=False)
        context['mediaUrl'] = settings.CLOUDINARY_URL if settings.USE_CLOUDINARY else settings.MEDIA_URL
        context['coralTalkServerUrl'] = settings.CORAL_TALK_SERVER_URL
        context['pageTitle'] = f'''{pgettext(
          'This can be localized. This is a reference to the “*batteries not included” mention on toys.',
          '*privacy not included'
        )} - {self.title}'''
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
    # NullBooleanField is deprecated as of Django 3.1.
    # We're using it here primarily for a data migration, but we should
    # move to BooleanField as soon as it's safe to do so with the content we have
    medical_privacy_compliant = models.NullBooleanField(
        null=True,
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
    # NullBooleanField is deprecated as of Django 3.1.
    # We're using it here primarily for a data migration, but we should
    # move to BooleanField as soon as it's safe to do so with the content we have
    easy_to_learn_and_use = models.NullBooleanField(
        null=True,
        help_text='Is it easy to learn & use the features?',
    )

    easy_to_learn_and_use_helptext = models.TextField(
        max_length=5000,
        blank=True
    )

    content_panels = ProductPage.content_panels.copy()
    content_panels = insert_panels_after(
        content_panels,
        'General Product Details',
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

    track_record_choices = [
        ('Great', 'Great'),
        ('Average', 'Average'),
        ('Needs Improvement', 'Needs Improvement'),
        ('Bad', 'Bad')
    ]

    company_track_record = models.CharField(
        choices=track_record_choices,
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

    # administrative panels

    content_panels = ProductPage.content_panels.copy()
    content_panels = insert_panels_after(
        content_panels,
        'General Product Details',
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

    class Meta:
        verbose_name = "General Product Page"


class BuyersGuidePage(RoutablePageMixin, FoundationMetadataPageMixin, Page):
    """
    Note: We'll likely be converting the "about" pages to Wagtail Pages.
    When that happens, we should remove the RoutablePageMixin and @routes
    """

    template = 'buyersguide/home.html'
    subpage_types = [SoftwareProductPage, GeneralProductPage]

    @route(r'^about/$', name='how-to-use-view')
    def about_page(self, request):
        self.template = "about/how_to_use.html"
        return self.serve(request)

    @route(r'^about/why/$', name='about-why-view')
    def about_why_page(self, request):
        self.template = "about/why_we_made.html"
        return self.serve(request)

    @route(r'^about/press/$', name='press-view')
    def about_press_page(self, request):
        self.template = "about/press.html"
        return self.serve(request)

    @route(r'^about/contact/$', name='contact-view')
    def about_contact_page(self, request):
        self.template = "about/contact.html"
        return self.serve(request)

    @route(r'^about/methodology/$', name='methodology-view')
    def about_methodology_page(self, request):
        self.template = "about/methodology.html"
        return self.serve(request)

    @route(r'^about/meets-minimum-security-standards/$', name='min-security-view')
    def about_mss_page(self, request):
        self.template = "about/minimum_security.html"
        return self.serve(request)

    @route(r'^products/(?P<slug>[-\w\d]+)/$', name='product-view')
    def product_view(self, request, slug):
        # Find product by it's slug and redirect to the product page
        # If no product is found, redirect to the BuyersGuide page
        product = get_object_or_404(ProductPage, slug=slug)
        return redirect(product.url)

    @route(r'^categories/(?P<slug>[\w\W]+)/', name='category-view')
    def categories_page(self, request, slug):
        # If getting by slug fails, also try to get it by name.
        try:
            category = BuyersGuideProductCategory.objects.get(slug=slug)
        except BuyersGuideProductCategory.DoesNotExist:
            category = get_object_or_404(BuyersGuideProductCategory, name__iexact=slug)

        products = ProductPage.objects.filter(product_categories__category__in=[category]).live()
        products = sort_average(products)
        products = cache.get_or_set('sorted_product_dicts', products, 86400)

        context = self.get_context(request)
        context['category'] = category.slug
        context['products'] = products
        context['pageTitle'] = pgettext(
                'This can be localized. This is a reference to the “*batteries not included” mention on toys.',
                '*privacy not included') + f' - {category}'
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
        if request.user.is_authenticated:
            products = ProductPage.objects.all()
        else:
            products = ProductPage.objects.live()

        products = sort_average(products)
        products = cache.get_or_set('sorted_product_dicts', products, 86400)

        context['categories'] = BuyersGuideProductCategory.objects.filter(hidden=False)
        context['products'] = products
        context['web_monetization_pointer'] = settings.WEB_MONETIZATION_POINTER
        return context

    class Meta:
        verbose_name = "Buyers Guide Page"
