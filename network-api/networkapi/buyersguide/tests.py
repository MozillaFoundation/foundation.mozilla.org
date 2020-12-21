import json
import logging

from django.contrib.auth.models import User
from django.core.management import call_command
from django.http import Http404
from django.urls import reverse
from django.utils.text import slugify
from django.test.utils import override_settings
from rest_framework.test import APITestCase
from django.test import TestCase, RequestFactory
from datetime import date
from unittest import skip

from networkapi.buyersguide.factory import ProductFactory
from networkapi.buyersguide.models import (
    RangeVote,
    BooleanVote,
    GeneralProduct,
    BuyersGuideProductCategory
)
from networkapi.buyersguide.views import product_view, category_view, buyersguide_home

from networkapi.wagtailpages.factory.homepage import WagtailHomepageFactory
from networkapi.wagtailpages.pagemodels.base import Homepage
from networkapi.wagtailpages.pagemodels.products import (
    BuyersGuidePage,
    ProductPage,
    ProductPageVotes,
    ProductPageCategory,
)

from wagtail.core.models import Page, Site
from wagtail.tests.utils import WagtailPageTests

VOTE_URL = reverse('product-vote')


class ManagementCommandTest(APITestCase):

    def test_votes_before_management_command_has_run(self):
        """
        Test that the votes attribute is None when there is no aggregated vote data for it
        """

        product = ProductFactory.create()
        self.assertIsNone(product.votes)

    def test_aggregate_product_votes_default(self):
        """
        Test that aggregate_product_votes provides default vote data for a product with no votes
        """
        product = ProductFactory.create()

        call_command('aggregate_product_votes')

        self.assertDictEqual(product.votes, {
            'creepiness': {
                'average': 50,
                'vote_breakdown': {
                    '0': 0,
                    '1': 0,
                    '2': 0,
                    '3': 0,
                    '4': 0
                }
            },
            'confidence': {
                '0': 0,
                '1': 0
            },
            'total': 0
        })

    def test_aggregate_product_votes(self):
        """
        Test that aggregate_product_votes properly aggregates votes
        """

        product = ProductFactory.create(draft=False)
        test_product_id = product.id
        request_data = {
            'attribute': 'creepiness',
            'productID': test_product_id
        }

        # Make 10 creepiness votes
        for i in (1, 10, 20, 30, 40, 50, 60, 70, 80, 90):
            request_data['value'] = i
            response = self.client.post(VOTE_URL, request_data, format='json')
            self.assertEqual(response.status_code, 201)

        request_data['attribute'] = 'confidence'
        for value in (True, False):
            request_data['value'] = value
            for _ in range(5):
                response = self.client.post(VOTE_URL, request_data, format='json')
                self.assertEqual(response.status_code, 201)

        call_command('aggregate_product_votes')

        self.assertDictEqual(product.votes, {
            'creepiness': {
                'average': 45,
                'vote_breakdown': {
                    '0': 3,
                    '1': 2,
                    '2': 2,
                    '3': 2,
                    '4': 1
                }
            },
            'confidence': {
                '0': 5,
                '1': 5
            },
            'total': 10
        })


class BuyersGuideVoteTest(APITestCase):

    def test_can_vote_range(self):
        """
        Range votes are recorded
        """

        test_product_id = ProductFactory.create(draft=False).id
        vote_value = 50

        response = self.client.post(VOTE_URL, {
            'attribute': 'creepiness',
            'value': vote_value,
            'productID': test_product_id
        }, format='json')

        self.assertEqual(response.status_code, 201)

        latest_vote = RangeVote.objects.last()

        self.assertEqual(latest_vote.value, vote_value)
        self.assertEqual(latest_vote.product.id, test_product_id)

    def test_can_vote_bool(self):
        """
        Boolean votes are recorded
        """
        test_product_id = ProductFactory.create(draft=False).id
        vote_value = True

        response = self.client.post(VOTE_URL, {
            'attribute': 'confidence',
            'value': vote_value,
            'productID': test_product_id
        }, format='json')
        latest_vote = BooleanVote.objects.last()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(latest_vote.value, vote_value)
        self.assertEqual(latest_vote.product.id, test_product_id)

    def test_invalid_values(self):
        """
        Value can't be anything other than a Boolean or int
        """
        test_product_id = ProductFactory.create(draft=False).id
        # String values not allowed
        vote_value = 'invalid'

        response = self.client.post(VOTE_URL, {
            'attribute': 'confidence',
            'value': vote_value,
            'productID': test_product_id
        }, format='json')

        self.assertEqual(response.status_code, 400)

        # Floating point numbers not allowed
        vote_value = 14.5
        response = self.client.post(VOTE_URL, {
            'attribute': 'creepiness',
            'value': vote_value,
            'productID': test_product_id
        }, format='json')

        self.assertEqual(response.status_code, 400)

        # undefined values not allowed
        response = self.client.post(VOTE_URL, {
            'attribute': 'creepiness',
            'value': None,
            'productID': test_product_id
        }, format='json')

        self.assertEqual(response.status_code, 400)

    def test_invalid_productID(self):
        """
        productID must be an int, and must exist in the database
        """
        test_product_id = '1'
        vote_value = 50

        response = self.client.post(VOTE_URL, {
            'attribute': 'creepiness',
            'value': vote_value,
            'productID': test_product_id
        }, format='json')

        self.assertEqual(response.status_code, 400)

        # Test an id that won't exist
        test_product_id = 100000000

        response = self.client.post(VOTE_URL, {
            'attribute': 'creepiness',
            'value': vote_value,
            'productID': test_product_id
        }, format='json')

        self.assertEqual(response.status_code, 400)

    def test_range_value_out_of_range(self):
        """
        If value is an int, it must be between 1 and 100
        """
        test_product_id = ProductFactory.create(draft=False).id
        vote_value = 0

        response = self.client.post(VOTE_URL, {
            'attribute': 'creepiness',
            'value': vote_value,
            'productID': test_product_id
        }, format='json')

        self.assertEqual(response.status_code, 400)

        test_product_id = ProductFactory.create(draft=False).id
        vote_value = 101

        response = self.client.post(VOTE_URL, {
            'attribute': 'creepiness',
            'value': vote_value,
            'productID': test_product_id
        }, format='json')

        self.assertEqual(response.status_code, 400)

    def test_invalid_attribute_with_int(self):
        """
        Test that attribute can only be 'creepiness' when value is an int
        """
        test_product_id = ProductFactory.create(draft=False).id
        vote_value = 50

        response = self.client.post(VOTE_URL, {
            'attribute': 'creepiness',
            'value': vote_value,
            'productID': test_product_id
        }, format='json')

        self.assertEqual(response.status_code, 201)

        test_product_id = ProductFactory.create(draft=False).id

        response = self.client.post(VOTE_URL, {
            'attribute': 'confidence',
            'value': vote_value,
            'productID': test_product_id
        }, format='json')

        self.assertEqual(response.status_code, 400)

    def test_invalid_attribute_with_boolean(self):
        """
        Test that attribute can only be 'confidence' when value is a boolean
        """
        test_product_id = ProductFactory.create(draft=False).id
        vote_value = True

        response = self.client.post(VOTE_URL, {
            'attribute': 'confidence',
            'value': vote_value,
            'productID': test_product_id
        }, format='json')

        self.assertEqual(response.status_code, 201)

        test_product_id = ProductFactory.create(draft=False).id

        response = self.client.post(VOTE_URL, {
            'attribute': 'creepiness',
            'value': vote_value,
            'productID': test_product_id
        }, format='json')

        self.assertEqual(response.status_code, 400)

    def test_missing_payload_attributes(self):
        """
        Test that missing attributes are handled
        """
        test_product_id = ProductFactory.create().id
        vote_value = True

        # no attribute
        response = self.client.post(VOTE_URL, {
            'value': vote_value,
            'productID': test_product_id
        }, format='json')

        self.assertEqual(response.status_code, 400)

        # no value
        response = self.client.post(VOTE_URL, {
            'attribute': 'confidence',
            'productID': test_product_id
        }, format='json')

        self.assertEqual(response.status_code, 400)

        # no productID
        response = self.client.post(VOTE_URL, {
            'attribute': 'confidence',
            'value': vote_value
        }, format='json')

        self.assertEqual(response.status_code, 400)


@override_settings(STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage")
class BuyersGuideViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testuser password'
        )

    def test_homepage(self):
        """
        Test that the homepage works.
        """
        request = self.factory.get('/en/privacynotincluded/')
        request.user = self.user
        response = buyersguide_home(request)
        self.assertEqual(response.status_code, 200, 'homepage yields a working page')

    @skip("TODO: REENABLE: THIS HAS BEEN TESTED MANUALLY BUT FAILS IN THIS CODE FORM ATM")
    def test_localised_homepage(self):
        """
        Test that the homepage redirects properly under different locale configurations.
        """
        response = self.client.get('/privacynotincluded/')
        self.assertEqual(response.status_code, 302, 'simple locale gets redirected')

        response = self.client.get('/privacynotincluded', follow=True, HTTP_ACCEPT_LANGUAGE='fr')
        self.assertEqual(
            response.redirect_chain[0][0],
            '/fr/privacynotincluded/',
            'redirects according to HTTP_ACCEPT_LANGUAGE'
        )
        self.assertEqual(response.status_code, 302)

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
        request = self.factory.get('/en/privacynotincluded/products/this is not a product')
        self.assertRaises(Http404, product_view, request, 'this is not a product')

    @skip("TODO: REMOVE: OLD MODEL TEST")
    def test_product_view(self):
        """
        Test that the product view returns a 200
        """
        p = GeneralProduct.objects.create(name='test product view', review_date=date.today())

        logger = logging.getLogger('django.request')
        previous_level = logger.getEffectiveLevel()
        logger.setLevel(logging.ERROR)
        response = self.client.get(f'/en/privacynotincluded/products/{p.slug}/')
        self.assertEqual(response.status_code, 404, 'The product should be a draft and so should not have a legal URL')
        logger.setLevel(previous_level)

        p.draft = False
        p.save()

        response = self.client.get(f'/en/privacynotincluded/products/{p.slug}/')
        self.assertEqual(response.status_code, 200, 'The product view should render once no longer a draft')

    def test_category_view_404(self):
        """
        Test that the category view raises an Http404 if the category name doesn't exist
        """
        request = self.factory.get('/en/privacynotincluded/categories/this is not a category')
        self.assertRaises(Http404, category_view, request, 'this is not a category')

    def test_category_view(self):
        """
        Test that the category view returns a 200 for both slug and name URLs
        """
        response = self.client.get('/privacynotincluded/categories/Smart%20Home/')
        self.assertEqual(response.status_code, 302, 'The category "Smart Home" should work by name')

        response = self.client.get('/privacynotincluded/categories/smart-home/')
        self.assertEqual(response.status_code, 302, 'The category "Smart Home" should work by slug')

    def test_drive_by_clear_cache(self):
        """
        regular users should not be able to trigger clear_cache
        """
        authenticated = self.user.is_authenticated

        self.client.logout()
        response = self.client.post('/api/buyersguide/clear-cache/')
        self.assertEqual(response.status_code, 403, 'standard user is not permitted to clear BG cache')

        if authenticated is True:
            self.client.force_login(self.user)

    def test_authenticated_clear_cache(self):
        """
        authenticated users can trigger clear_cache
        """
        authenticated = self.user.is_authenticated

        self.client.force_login(self.user)
        response = self.client.post('/api/buyersguide/clear-cache/')
        self.assertEqual(response.status_code, 302, 'authenticated user is permitted to clear BG cache')
        self.assertEqual(response.url, '/cms/', 'clearing sends users to product page')

        if authenticated is False:
            self.client.logout()


@override_settings(STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage")
class ProductTests(TestCase):
    def test_product_slug(self):
        p = GeneralProduct.objects.create(name='this name should get slugified', review_date=date.today())
        self.assertEqual(p.slug, slugify(p.name))

    def name_change_changes_slug(self):
        p = GeneralProduct.objects.create(name='this will change', review_date=date.today())
        p.name = 'name changed'
        p.save()
        self.assertEqual(p.slug, slugify(p.name))


class BuyersGuideTestMixin(WagtailPageTests):

    def setUp(self):
        # Ensure there's always a BuyersGuide Page
        self.bg = self.get_or_create_buyers_guide()
        self.product_page = self.get_or_create_product_page()

        site = Site.objects.first()
        site.root_page = self.homepage
        site.save()

    def get_or_create_buyers_guide(self):
        """
        Return the first BuyersGuidePage, or create a new one.
        Will generate a Homepage if needed.
        """
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
            # Create the buyersguide page.
            buyersguide = BuyersGuidePage()
            buyersguide.title = 'Privacy not included'
            buyersguide.slug = 'privacynotincluded-new'
            buyersguide.slug_en = 'privacynotincluded-new'
            homepage = Homepage.objects.first()
            homepage.add_child(instance=buyersguide)
            buyersguide.save_revision().publish()
        self.homepage = Homepage.objects.first()
        return buyersguide

    def get_or_create_product_page(self):
        product_page = ProductPage.objects.first()
        if not product_page:
            product_page = ProductPage(
                slug='product-page',
                slug_en='product-page',
                title='Product Page',
                title_en='Product Page',
                live=True,
            )
            self.bg.add_child(instance=product_page)
            product_page.save_revision().publish()
        return product_page


@override_settings(STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage")
class TestBuyersGuidePage(BuyersGuideTestMixin):

    def test_buyersguide_url(self):
        self.assertEqual(self.bg.slug, 'privacynotincluded-new')
        response = self.client.get(self.bg.url)
        self.assertEqual(response.status_code, 200)

    def about_url_test(self, view_name, target_url, template):
        url = self.bg.reverse_subpage(view_name)
        self.assertEqual(url, target_url)
        response = self.client.get(self.bg.url + url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, f'about/{template}.html')

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

    def test_buyersguide_about_mss_view(self):
        self.about_url_test('min-security-view', 'about/meets-minimum-security-standards/', 'minimum_security')

    def test_contest_page(self):
        url = self.bg.reverse_subpage('contest')
        self.assertEqual(url, 'contest/')
        response = self.client.get(self.bg.url + url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contest.html')

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
        response = self.client.get('/sitemap.xml')
        context = response.context

        self.assertEqual(context.template_name, 'sitemap.xml')
        self.assertContains(response, 'about/')
        self.assertContains(response, 'about/why/')
        self.assertContains(response, 'about/press/')
        self.assertContains(response, 'about/contact/')
        self.assertContains(response, 'about/methodology/')
        self.assertContains(response, 'about/meets-minimum-security-standards/')

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
            self.assertEqual(len(response.context['products']), 0)

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


class TestProductPage(BuyersGuideTestMixin):

    def setUp(self):
        super().setUp()
        if not hasattr(self.product_page.votes, 'get_votes'):
            votes = ProductPageVotes()
            votes.save()
            self.product_page.votes = votes
            self.product_page.save()

    def test_get_votes(self):
        # Votes should be empty at this point.
        votes = self.product_page.votes.get_votes()
        self.assertEqual(votes, [0, 0, 0, 0, 0])
        self.assertEqual(len(votes), 5)

    def test_set_votes(self):
        # Make sure votes are set and saved.
        self.product_page.votes.set_votes([1, 2, 3, 4, 5])
        votes = self.product_page.votes.get_votes()
        self.assertEqual(votes, [1, 2, 3, 4, 5])

        # Ensure there's always 5 value set.
        self.product_page.votes.set_votes([1, 2, 3, 4, 5, 6, 7])
        self.assertEqual(votes, [1, 2, 3, 4, 5])
        self.assertEqual(len(votes), 5)

    def test_total_vote_count(self):
        self.product_page.votes.set_votes([5, 4, 3, 2, 1])
        total_vote_count = self.product_page.total_vote_count
        self.assertEqual(total_vote_count, 15)

        self.product_page.votes.set_votes([5, 5, 5, 5, 5])
        total_vote_count = self.product_page.total_vote_count
        self.assertEqual(total_vote_count, 25)

    def test_creepiness(self):
        self.product_page.creepiness_value = 100
        self.product_page.votes.set_votes([5, 5, 5, 5, 5])
        creepiness = self.product_page.creepiness
        self.assertEqual(creepiness, 4)

        self.product_page.creepiness_value = 0
        self.product_page.votes.set_votes([0, 0, 0, 0, 0])
        creepiness = self.product_page.creepiness
        self.assertEqual(creepiness, 50)

    def test_get_voting_json(self):
        self.product_page.creepiness_value = 60
        self.product_page.votes.set_votes([1, 2, 3, 4, 5])
        creepiness = self.product_page.creepiness
        self.assertEqual(creepiness, 4)

        total_vote_count = self.product_page.total_vote_count
        self.assertEqual(total_vote_count, 15)

        # votes = self.product_page.votes.get_votes()
        data = json.loads(self.product_page.get_voting_json)
        comparable_data = {
            'creepiness': {
                'vote_breakdown':  {
                    '0': 1,
                    '1': 2,
                    '2': 3,
                    '3': 4,
                    '4': 5,
                },
                'average': 4.0,
            },
            'total': 15,
        }
        self.assertDictEqual(data, comparable_data)

    def test_get_or_create_votes(self):
        # Delete potential votes
        self.product_page.votes.delete()
        self.product_page.votes = None
        self.assertEqual(self.product_page.votes, None)

        votes = self.product_page.get_or_create_votes()
        self.assertEqual(votes, [0, 0, 0, 0, 0])
        self.assertTrue(hasattr(self.product_page.votes, 'set_votes'))


@override_settings(STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage")
class WagtailBuyersGuideVoteTest(APITestCase, BuyersGuideTestMixin):

    def test_successful_vote(self):
        # Reset votes
        votes = self.product_page.get_or_create_votes()
        self.product_page.votes.set_votes([0, 0, 0, 0, 0])

        response = self.client.post(self.product_page.url, {
            'value': 25,
        }, format='json')
        self.assertEqual(response.status_code, 200)

        self.product_page.refresh_from_db()

        votes = self.product_page.votes.get_votes()
        self.assertListEqual(votes, [0, 1, 0, 0, 0])
        self.assertEqual(self.product_page.total_vote_count, 1)
        self.assertEqual(self.product_page.creepiness_value, 25)

        response = self.client.post(self.product_page.url, {
            'value': 100,
        }, format='json')
        self.assertEqual(response.status_code, 200)

        self.product_page.refresh_from_db()

        votes = self.product_page.votes.get_votes()
        self.assertListEqual(votes, [0, 1, 0, 0, 1])
        self.assertEqual(self.product_page.total_vote_count, 2)
        self.assertEqual(self.product_page.creepiness_value, 125)

    def test_bad_vote_value(self):
        # vote = 500
        response = self.client.post(self.product_page.url, {
            'value': -1,
        }, format='json')
        self.assertEqual(response.status_code, 405)

        response = self.client.post(self.product_page.url, {
            'value': 101,
        }, format='json')
        self.assertEqual(response.status_code, 405)

    def test_vote_on_draft_page(self):
        self.product_page.live = False
        self.product_page.save()

        response = self.client.post(self.product_page.url, {
            'value': 25,
            'productID': self.product_page.id
        }, format='json')
        self.assertEqual(response.status_code, 404)

        # Reset the page back to Live
        self.product_page.live = True
        self.product_page.save()
