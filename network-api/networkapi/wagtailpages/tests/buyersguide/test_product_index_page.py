import http

from django import test

from networkapi.wagtailpages.tests.buyersguide import base as test_base
from networkapi.wagtailpages.pagemodels.buyersguide import (
    homepage,
    product_index_page,
    products,
)
from networkapi.wagtailpages.factory import buyersguide as buyersguide_factories


class TestFactories(test.TestCase):
    def test_index_page_factory(self):
        buyersguide_factories.ProductIndexPageFactory()


class TestProductIndexPage(test_base.BuyersGuideTestCase):
    def test_buyersguide_homepage_as_parent(self):
        self.assertCanCreateAt(
            child_model=product_index_page.ProductIndexPage,
            parent_model=homepage.BuyersGuidePage,
        )

    def test_product_pages_as_child_pages(self):
        self.assertCanCreateAt(
            child_model=products.GeneralProductPage,
            parent_model=product_index_page.ProductIndexPage,
        )

    def test_redirects_to_parent(self):
        response = self.client.get(self.product_index_page.get_url())

        self.assertEqual(response.status_code, http.HTTPStatus.FOUND)
        self.assertEqual(response.headers["Location"], self.bg.get_url())
