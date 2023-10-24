from networkapi.wagtailpages.factory import buyersguide as buyersguide_factories
from networkapi.wagtailpages.pagemodels.buyersguide.products import (
    BuyersGuideProductCategory,
    ProductPage,
    ProductPageCategory,
)
from networkapi.wagtailpages.tests.buyersguide.base import BuyersGuideTestCase


class TestBuyersGuideProductCategory(BuyersGuideTestCase):
    def test_published_product_page_count(self):
        # Create category
        category = buyersguide_factories.BuyersGuideProductCategoryFactory()
        # Create product pages
        product_page_a = buyersguide_factories.ProductPageFactory()
        product_page_b = buyersguide_factories.ProductPageFactory()
        product_page_not_live = buyersguide_factories.ProductPageFactory(live=False)
        product_page_not_linked = buyersguide_factories.ProductPageFactory()
        # Link product pages to category
        buyersguide_factories.ProductPageCategoryFactory(product=product_page_a, category=category)
        buyersguide_factories.ProductPageCategoryFactory(product=product_page_b, category=category)
        buyersguide_factories.ProductPageCategoryFactory(product=product_page_not_live, category=category)

        products = category.published_product_pages

        self.assertIn(product_page_a, products)
        self.assertIn(product_page_b, products)
        self.assertNotIn(product_page_not_live, products)
        self.assertNotIn(product_page_not_linked, products)

        # There should be 2 published product pages (product_page_a and product_page_b)
        self.assertEqual(category.published_product_page_count, 2)

    def test_published_product_page_count_with_prefetching(self):
        BuyersGuideProductCategory.objects.all().delete()

        # Create product pages
        valid_product_pages = []
        for _ in range(20):
            valid_product_pages.append(buyersguide_factories.ProductPageFactory(live=True))
        product_page_not_live = buyersguide_factories.ProductPageFactory(live=False)
        product_page_not_linked = buyersguide_factories.ProductPageFactory()

        for _ in range(5):
            # Create category
            category = buyersguide_factories.BuyersGuideProductCategoryFactory()
            # Link product pages to category
            for product_page in valid_product_pages:
                buyersguide_factories.ProductPageCategoryFactory(product=product_page, category=category)
            buyersguide_factories.ProductPageCategoryFactory(product=product_page_not_live, category=category)

        query_number = 5 + 3  # 1 query for each category, 3 general queries

        with self.assertNumQueries(query_number):
            categories = BuyersGuideProductCategory.objects.all().with_published_product_pages()
            for category in categories:
                products = category.published_product_pages
                self.assertNotIn(product_page_not_live, products)
                self.assertNotIn(product_page_not_linked, products)
                self.assertEqual(category.published_product_page_count, 20)
