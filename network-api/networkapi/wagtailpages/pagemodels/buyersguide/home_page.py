from datetime import datetime

from django.apps import apps
from django.conf import settings
from django.db import models
from django.core.cache import cache
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify
from django.utils.translation import gettext, pgettext
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.models import Locale, Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail_localize.fields import SynchronizedField, TranslatableField

from networkapi.wagtailpages.pagemodels.mixin.foundation_metadata import (
    FoundationMetadataPageMixin
)
from networkapi.wagtailpages.templatetags.localization import relocalize_url
from networkapi.wagtailpages.utils import (
    get_default_locale,
    get_language_from_request,
    get_locale_from_request,
)
from networkapi.wagtailpages.pagemodels.buyersguide.utils import (
    get_categories_for_locale,
    sort_average,
)


class BuyersGuidePage(RoutablePageMixin, FoundationMetadataPageMixin, Page):
    """
    Note: We'll likely be converting the "about" pages to Wagtail Pages.
    When that happens, we should remove the RoutablePageMixin and @routes
    """

    template = 'pages/buyersguide/home.html'
    subpage_types = [
        'wagtailpages.GeneralProductPage',
        'wagtailpages.BuyersGuideEditorialContentIndexPage',
    ]

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
        SynchronizedField('cutoff_date'),
        SynchronizedField('hero_image'),
        TranslatableField('header'),
        TranslatableField('intro_text'),
        SynchronizedField('dark_theme'),
        SynchronizedField('excluded_categories'),
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
        return render(request, "pages/buyersguide/how_to_use.html", context)

    @route(r'^about/why/$', name='about-why-view')
    def about_why_page(self, request):
        context = self.get_context(request)
        context['pagetype'] = 'about'
        context['pageTitle'] = pgettext(
            '*privacy not included can be localized.',
            'Why we made *privacy not included')
        return render(request, "pages/buyersguide/why_we_made.html", context)

    @route(r'^about/press/$', name='press-view')
    def about_press_page(self, request):
        context = self.get_context(request)
        context['pagetype'] = 'about'
        context['pageTitle'] = pgettext('Noun, media', 'Press') + ' | ' + pgettext(
            'This can be localized. This is a reference to the “*batteries not included” mention on toys.',
            '*privacy not included')
        return render(request, "pages/buyersguide/press.html", context)

    @route(r'^about/contact/$', name='contact-view')
    def about_contact_page(self, request):
        context = self.get_context(request)
        context['pagetype'] = 'about'
        context['pageTitle'] = gettext('Contact us') + ' | ' + pgettext(
            'This can be localized. This is a reference to the “*batteries not included” mention on toys.',
            '*privacy not included')
        return render(request, "pages/buyersguide/contact.html", context)

    @route(r'^about/methodology/$', name='methodology-view')
    def about_methodology_page(self, request):
        context = self.get_context(request)
        context['pagetype'] = 'about'
        context['pageTitle'] = gettext('Our methodology') + ' | ' + pgettext(
            'This can be localized. This is a reference to the “*batteries not included” mention on toys.',
            '*privacy not included')
        return render(request, "pages/buyersguide/methodology.html", context)

    @route(r'^contest/$', name='contest')
    def about_contest(self, request):
        context = self.get_context(request)
        context['pagetype'] = 'contest'
        context['pageTitle'] = gettext('Contest terms and conditions') + ' | ' + pgettext(
            'This can be localized. This is a reference to the “*batteries not included” mention on toys.',
            '*privacy not included')
        return render(request, "pages/buyersguide/contest.html", context)

    @route(r'^products/(?P<slug>[-\w\d]+)/$', name='product-view')
    def product_view(self, request, slug):
        # Find product by it's slug and redirect to the product page
        # If no product is found, redirect to the BuyersGuide page
        locale = get_locale_from_request(request)
        ProductPage = apps.get_model(app_label='wagtailpages', model_name='ProductPage')
        product = get_object_or_404(ProductPage, slug=slug, locale=locale)
        url = relocalize_url(product.url, locale.language_code)
        return redirect(url)

    @route(r'^categories/(?P<slug>[\w\W]+)/', name='category-view')
    def categories_page(self, request, slug):
        context = self.get_context(request, bypass_products=True)
        language_code = get_language_from_request(request)
        locale_id = Locale.objects.get(language_code=language_code).id
        slug = slugify(slug)

        (DEFAULT_LOCALE, DEFAULT_LOCALE_ID) = get_default_locale()

        # because we may be working with localized content, and the slug
        # will always be our english slug, we need to find the english
        # category first, and then find its corresponding localized version
        BuyersGuideProductCategory = apps.get_model(
            app_label='wagtailpages',
            model_name='BuyersGuideProductCategory',
        )
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

        ProductPage = apps.get_model(app_label='wagtailpages', model_name='ProductPage')
        if products is None:
            products = get_product_subset(
                self.cutoff_date,
                authenticated,
                key,
                ProductPage.objects.exclude(product_categories__category__id__in=exclude_cat_ids),
                language_code=language_code
            )

        context['category'] = slug
        context['current_category'] = category
        context['products'] = products
        context['pageTitle'] = f'{category.localized.name} | {gettext("Privacy & security guide")}'\
                               f' | Mozilla Foundation'
        context['template_cache_key_fragment'] = f'{category.slug}_{request.LANGUAGE_CODE}'

        # Checking if category has custom metadata, if so, update the share image and description.
        if category.share_image:
            setattr(self, 'search_image_id', category.localized.share_image_id)
        if category.description:
            setattr(self, 'search_description', category.localized.description)

        return render(request, "pages/buyersguide/category_page.html", context)

    def get_sitemap_urls(self, request):
        """
        Add categories and route views to the sitemap for better search indexing.
        """
        sitemap = super().get_sitemap_urls(request)
        last_modified = self.last_published_at or self.latest_revision_created_at
        # Add all the available Buyers Guide categories to the sitemap
        BuyersGuideProductCategory = apps.get_model(app_label='wagtailpages', model_name='BuyersGuideProductCategory')
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
            'contact-view', 'methodology-view'
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

        ProductPage = apps.get_model(app_label='wagtailpages', model_name='ProductPage')
        if not kwargs.get('bypass_products', False) and products is None:
            products = get_product_subset(
                self.cutoff_date,
                authenticated,
                key,
                ProductPage.objects.exclude(product_categories__category__id__in=exclude_cat_ids),
                language_code=language_code
            )

        context['categories'] = get_categories_for_locale(language_code)
        context['current_category'] = None
        context['products'] = products
        context['web_monetization_pointer'] = settings.WEB_MONETIZATION_POINTER
        pni_home_page = BuyersGuidePage.objects.first()
        context['about_page'] = pni_home_page
        context['home_page'] = pni_home_page
        context['template_cache_key_fragment'] = f'pni_home_{request.LANGUAGE_CODE}'
        return context

    def get_editorial_content_index(self):
        BuyersGuideEditorialContentIndexPage = apps.get_model(
            app_label='wagtailpages',
            model_name='BuyersGuideEditorialContentIndexPage',
        )
        indexes = BuyersGuideEditorialContentIndexPage.objects.descendant_of(self)
        return indexes.first()

    class Meta:
        verbose_name = "Buyers Guide Page"


def get_pni_home_page():
    """
    Used in AIRTABLE settings for nesting child pages under a new parent page.
    """
    return BuyersGuidePage.objects.first().id


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
