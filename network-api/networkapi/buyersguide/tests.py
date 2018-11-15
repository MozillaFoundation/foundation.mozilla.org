from django.contrib.auth.models import User
from django.http import Http404
from django.urls import reverse
from django.utils.text import slugify
from rest_framework.test import APITestCase
from django.test import TestCase, RequestFactory

from networkapi.buyersguide.factory import ProductFactory
from networkapi.buyersguide.models import RangeVote, BooleanVote, Product, BuyersGuideProductCategory
from networkapi.buyersguide.views import product_view, category_view, buyersguide_home
from django.core.management import call_command

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

        product = ProductFactory.create()
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

        test_product_id = ProductFactory.create().id
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
        test_product_id = ProductFactory.create().id
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
        test_product_id = ProductFactory.create().id
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
        test_product_id = ProductFactory.create().id
        vote_value = 0

        response = self.client.post(VOTE_URL, {
            'attribute': 'creepiness',
            'value': vote_value,
            'productID': test_product_id
        }, format='json')

        self.assertEqual(response.status_code, 400)

        test_product_id = ProductFactory.create().id
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
        test_product_id = ProductFactory.create().id
        vote_value = 50

        response = self.client.post(VOTE_URL, {
            'attribute': 'creepiness',
            'value': vote_value,
            'productID': test_product_id
        }, format='json')

        self.assertEqual(response.status_code, 201)

        test_product_id = ProductFactory.create().id

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
        test_product_id = ProductFactory.create().id
        vote_value = True

        response = self.client.post(VOTE_URL, {
            'attribute': 'confidence',
            'value': vote_value,
            'productID': test_product_id
        }, format='json')

        self.assertEqual(response.status_code, 201)

        test_product_id = ProductFactory.create().id

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
        response = buyersguide_home(request)
        self.assertEqual(response.status_code, 200, 'homepage yields a working page')

    def test_localised_homepage(self):
        """
        Test that the homepage redirects when missing a locale code.
        """
        response = self.client.get('/privacynotincluded/')
        self.assertEqual(response.status_code, 302, 'simple locale gets redirected')

    def test_only_en(self):
        """
        Test that the homepage redirects away from the other locales the site supports
        """
        response = self.client.get('/fr/privacynotincluded', follow=True)
        self.assertEqual(response.redirect_chain[1][0], '/en/privacynotincluded/', 'redirects /fr/ to /en/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/de/privacynotincluded', follow=True)
        self.assertEqual(response.redirect_chain[1][0], '/en/privacynotincluded/', 'redirects /de/ to /en/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/pt/privacynotincluded', follow=True)
        self.assertEqual(response.redirect_chain[1][0], '/en/privacynotincluded/', 'redirects /pt/ to /en/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/es/privacynotincluded', follow=True)
        self.assertEqual(response.redirect_chain[1][0], '/en/privacynotincluded/', 'redirects /es/ to /en/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/pl/privacynotincluded', follow=True)
        self.assertEqual(response.redirect_chain[1][0], '/en/privacynotincluded/', 'redirects /pl/ to /en/')
        self.assertEqual(response.status_code, 200)

    def test_product_view_404(self):
        """
        Test that the product view raises an Http404 if the product name doesn't exist
        """
        request = self.factory.get('/en/privacynotincluded/products/this is not a product')
        self.assertRaises(Http404, product_view, request, 'this is not a product')

    def test_category_view_404(self):
        """
        Test that the category view raises an Http404 if the category name doesn't exist
        """
        request = self.factory.get('/en/privacynotincluded/categories/this is not a category')
        self.assertRaises(Http404, category_view, request, 'this is not a category')

    def test_product_view(self):
        """
        Test that the product view returns a 200
        """
        p = Product.objects.create(name='test product view')

        response = self.client.get(f'/en/privacynotincluded/products/{p.slug}/')
        self.assertEqual(response.status_code, 200, 'The product view should render')


class ProductTests(TestCase):
    def test_product_slug(self):
        p = Product.objects.create(name='this name should get slugified')
        self.assertEqual(p.slug, slugify(p.name))

    def name_change_changes_slug(self):
        p = Product.objects.create(name='this will change')
        p.name = 'name changed'
        p.save()
        self.assertEqual(p.slug, slugify(p.name))

    def test_only_en(self):
        p = Product.objects.create(name='this should redirect')
        url = f'/fr/privacynotincluded/products/{p.slug}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response['Location'],
            f'/en/privacynotincluded/products/{p.slug}/',
            'redirects to /en/privacynotincluded/products/{slug}/'
        )


class CategoryViewTest(TestCase):
    def test_only_en(self):
        c = BuyersGuideProductCategory.objects.create(name='testcategory')
        url = f'/fr/privacynotincluded/categories/{c.name}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response['Location'],
            f'/en/privacynotincluded/categories/{c.name}/',
            'redirects to /en/privacynotincluded/categories/{name}/'
        )


class AboutViewTest(TestCase):
    def test_only_en(self):
        url = f'/fr/privacynotincluded/about/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response['Location'],
            f'/en/privacynotincluded/about/',
            'redirects to /en/privacynotincluded/about/'
        )
