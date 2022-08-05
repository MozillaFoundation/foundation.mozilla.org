import json
from os.path import abspath, join

from django.conf import settings
from django.contrib.auth.models import User
from django.test.utils import override_settings
from rest_framework.test import APITestCase
from django.test import TestCase, RequestFactory

from networkapi.wagtailpages.factory.homepage import WagtailHomepageFactory
from networkapi.wagtailpages.factory import buyersguide as buyersguide_factories
from networkapi.wagtailpages.pagemodels.base import Homepage
from networkapi.wagtailpages.pagemodels.buyersguide.home_page import BuyersGuidePage
from networkapi.wagtailpages.pagemodels.buyersguide.products import (
    ProductPage,
    ProductPageVotes,
    ProductPageCategory,
    BuyersGuideProductCategory,
)
from networkapi.wagtailpages.tests.buyersguide.base import BuyersGuideTestMixin
from networkapi.wagtailpages.utils import create_wagtail_image

from wagtail.core.models import Page, Site
from wagtail.core.models.i18n import Locale
from wagtail.snippets.views.snippets import get_snippet_edit_handler
from wagtail.tests.utils import WagtailPageTests


@override_settings(STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage")
class BuyersGuideViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testuser password'
        )
        buyersguide = BuyersGuidePage.objects.first()
        if not buyersguide:
            homepage = Homepage.objects.first()
            if not homepage:
                site_root = Page.objects.first()
                homepage = WagtailHomepageFactory.create(
                    parent=site_root,
                    title='Homepage',
                    slug='homepage',
                    hero_image__file__width=1080,
                    hero_image__file__height=720
                )
            site = Site.objects.first()
            site.root_page = homepage
            site.save()
            # Create the buyersguide page.
            buyersguide = BuyersGuidePage()
            buyersguide.title = 'Privacy not included'
            buyersguide.slug = 'privacynotincluded'
            homepage.add_child(instance=buyersguide)
            buyersguide.save_revision().publish()

            locale = Locale.objects.create(language_code="fr")
            buyersguide.copy_for_translation(locale, copy_parents=True, alias=True)

    def test_homepage(self):
        """
        Test that the homepage works.
        """
        response = self.client.get('/privacynotincluded/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            '/en/privacynotincluded/',
            'Homepage should be forwarded to /en/ by default'
        )

    def test_localised_homepage(self):
        """
        Test that the homepage redirects properly under different locale configurations.
        """
        response = self.client.get('/privacynotincluded', follow=True, HTTP_ACCEPT_LANGUAGE='fr')
        self.assertEqual(
            response.redirect_chain[0][0],
            '/fr/privacynotincluded/',
            'redirects according to HTTP_ACCEPT_LANGUAGE'
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/privacynotincluded', follow=True, HTTP_ACCEPT_LANGUAGE='sw')
        self.assertEqual(
            response.redirect_chain[0][0],
            '/sw/privacynotincluded/',
            'redirects according to HTTP_ACCEPT_LANGUAGE for non-existent locale'
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/privacynotincluded', follow=True, HTTP_ACCEPT_LANGUAGE='foo')
        self.assertEqual(response.redirect_chain[0][0], '/en/privacynotincluded/', 'redirects to /en/ by default')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/de/privacynotincluded', follow=True, HTTP_ACCEPT_LANGUAGE='it')
        self.assertEqual(response.redirect_chain[0][0], '/de/privacynotincluded/', 'no redirect from hardcoded locale')
        self.assertEqual(response.status_code, 200)

    def test_product_view_404(self):
        """
        Test that the product view raises an Http404 if the product name doesn't exist
        """
        response = self.client.get('/en/privacynotincluded/products/this is not a product', follow=True)
        self.assertEqual(response.status_code, 404, 'this is not a product')

        response = self.client.get('/en/privacynotincluded/products/this is not a product/')
        self.assertEqual(response.status_code, 404, 'this is not a product')

    def test_category_view_404(self):
        """
        Test that the category view raises an Http404 if the category name doesn't exist
        """
        response = self.client.get('/en/privacynotincluded/categories/this is not a category', follow=True)
        self.assertEqual(response.status_code, 404, 'this is not a category')

        response = self.client.get('/en/privacynotincluded/categories/this is not a category/')
        self.assertEqual(response.status_code, 404, 'this is not a category')

    def test_category_view(self):
        """
        Test that the category view returns a 302 for /privacynotincluded/ to /en/privacynotincluded/
        for both slug-based and name-based categories.
        """
        response = self.client.get('/privacynotincluded/categories/Smart%20Home/')
        self.assertEqual(response.status_code, 302, 'The category "Smart Home" should work by name')

        response = self.client.get('/privacynotincluded/categories/smart-home/')
        self.assertEqual(response.status_code, 302, 'The category "Smart Home" should work by slug')


# Use dummy caching for BuyersGuide URLs.
@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}})
@override_settings(STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage")
class TestBuyersGuidePage(BuyersGuideTestMixin):

    def test_buyersguide_url(self):
        self.assertEqual(self.bg.slug, 'privacynotincluded')
        response = self.client.get(self.bg.url)
        self.assertEqual(response.status_code, 200)

    def about_url_test(self, view_name, target_url, template):
        url = self.bg.reverse_subpage(view_name)
        self.assertEqual(url, target_url)
        response = self.client.get(self.bg.url + url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, f'pages/buyersguide/{template}.html')

    def test_buyersguide_about_how_to_use_view(self):
        self.about_url_test('how-to-use-view', 'about/', 'how_to_use')

    def test_buyersguide_about_why_view(self):
        self.about_url_test('about-why-view', 'about/why/', 'why_we_made')

    def test_buyersguide_about_press_view(self):
        self.about_url_test('press-view', 'about/press/', 'press')

    def test_buyersguide_about_contact_view(self):
        self.about_url_test('contact-view', 'about/contact/', 'contact')

    def test_buyersguide_about_methodology_view(self):
        self.about_url_test('methodology-view', 'about/methodology/', 'methodology')

    def test_contest_page(self):
        url = self.bg.reverse_subpage('contest')
        self.assertEqual(url, 'contest/')
        response = self.client.get(self.bg.url + url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/buyersguide/contest.html')

    def test_buyersguide_category_route(self):
        # Missing category
        missing_category = 'missing-category-slug'
        category_url = self.bg.reverse_subpage('category-view', args=(missing_category,))
        self.assertEqual(category_url, f'categories/{missing_category}/')

        full_url = self.bg.url + category_url
        response = self.client.get(full_url)
        self.assertEqual(response.status_code, 404)

        category = BuyersGuideProductCategory.objects.first()
        response = self.client.get(f'/en/{self.bg.slug}/categories/{category.slug}/')
        self.assertEqual(response.status_code, 200)

    def test_buyersguide_product_redirect_route(self):
        response = self.client.get(self.bg.url)
        self.assertEqual(response.status_code, 200)

        product = self.get_or_create_product_page()
        response = self.client.get(product.url)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(f'/en/{self.bg.slug}/products/{product.slug}/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[0][0], product.url)

    def test_sitemap_entries(self):
        response = self.client.get('/en/sitemap.xml')
        context = response.context

        self.assertEqual(context.template_name, 'sitemap.xml')
        self.assertContains(response, 'about/')
        self.assertContains(response, 'about/why/')
        self.assertContains(response, 'about/press/')
        self.assertContains(response, 'about/contact/')
        self.assertContains(response, 'about/methodology/')

        categories = BuyersGuideProductCategory.objects.filter(hidden=False)
        for category in categories:
            self.assertContains(response, f'categories/{category.slug}/')

    def test_empty_products_url(self):
        products_page = self.bg.url + 'products/'
        response = self.client.get(products_page)
        self.assertEqual(response.status_code, 404)

    def test_empty_categories_url(self):
        categories_page = self.bg.url + 'categories/'
        response = self.client.get(categories_page)
        self.assertEqual(response.status_code, 404)

    def test_category_filter_view(self):
        category = BuyersGuideProductCategory.objects.first()
        url = self.bg.url + self.bg.reverse_subpage('category-view', args=(category.slug,))

        # Need to set dummy cache
        with self.settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}}):
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.context['products']), 1)

            # Add BuyersGuideProductCategory
            category_orderable = ProductPageCategory(
                product=self.product_page,
                category=category,
            )
            category_orderable.save()
            self.product_page.product_categories.add(category_orderable)
            self.product_page.save_revision().publish()

            response = self.client.get(url)
            self.assertEqual(len(response.context['products']), 1)

    def test_get_editorial_content_index(self):
        """Returns the editorial content index page."""
        editorial_content_index = buyersguide_factories.BuyersGuideEditorialContentIndexPageFactory(parent=self.bg)

        result = self.bg.get_editorial_content_index()

        self.assertEqual(result, editorial_content_index)

    def test_get_editorial_content_index_no_such_page(self):
        """Returns None when there is no editorial content index page."""
        result = self.bg.get_editorial_content_index()

        self.assertEqual(result, None)
