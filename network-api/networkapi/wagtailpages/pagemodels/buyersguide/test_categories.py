from networkapi.wagtailpages.factory import buyersguide as buyersguide_factories
from networkapi.wagtailpages.pagemodels.buyersguide.products import ProductPage
from networkapi.wagtailpages.tests.buyersguide.base import BuyersGuideTestCase


class TestBuyersGuideProductCategory(BuyersGuideTestCase):
    def test_published_product_page_count(self):
        # Create category
        category = buyersguide_factories.BuyersGuideProductCategoryFactory()
        # Create product pages
        product_page_a = buyersguide_factories.ProductPageFactory()
        product_page_b = buyersguide_factories.ProductPageFactory()
        product_page_not_live = buyersguide_factories.ProductPageFactory(live=False)
        self.assertFalse(product_page_not_live.live)
        product_page_not_linked = buyersguide_factories.ProductPageFactory()
        # Link product pages to category
        buyersguide_factories.ProductPageCategoryFactory(product=product_page_a, category=category)
        buyersguide_factories.ProductPageCategoryFactory(product=product_page_b, category=category)
        buyersguide_factories.ProductPageCategoryFactory(product=product_page_not_live, category=category)

        self.assertFalse(product_page_not_live.live)

        products = ProductPage.objects.filter(product_categories__category=category).live()

        self.assertIn(product_page_a, products)
        self.assertIn(product_page_b, products)
        self.assertNotIn(product_page_not_live, products)
        self.assertNotIn(product_page_not_linked, products)

        # There should be 2 published product pages (product_page_a and product_page_b)
        self.assertEqual(category.published_product_page_count, 2)
