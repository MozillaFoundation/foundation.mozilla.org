import unittest

from networkapi.wagtailpages.factory import buyersguide as buyersguide_factories
from networkapi.wagtailpages.pagemodels.buyersguide.products import (
    BuyersGuideProductCategory,
)
from networkapi.wagtailpages.tests.buyersguide.base import BuyersGuideTestCase


class TestPublishedProductPagesProperty(BuyersGuideTestCase):
    def setUp(self):
        super().setUp()
        self.admin_user = self.create_superuser(username="admin", password="password")
        self.login(self.admin_user)

    def test_published_product_page_count(self):
        # Create category
        category = buyersguide_factories.BuyersGuideProductCategoryFactory()
        # Create product pages
        product_page_a = buyersguide_factories.ProductPageFactory(parent=self.bg)
        product_page_b = buyersguide_factories.ProductPageFactory(parent=self.bg)
        product_page_not_live = buyersguide_factories.ProductPageFactory(live=False, parent=self.bg)
        product_page_not_linked = buyersguide_factories.ProductPageFactory(parent=self.bg)
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

    @unittest.expectedFailure  # the property can't localize the queryset yet
    def test_published_product_page_count_with_translated_pages(self):
        # Create category
        category = buyersguide_factories.BuyersGuideProductCategoryFactory()
        # Create product pages
        product_page_live = buyersguide_factories.ProductPageFactory(live=True, parent=self.bg)
        product_page_not_live = buyersguide_factories.ProductPageFactory(live=False, parent=self.bg)
        product_page_not_linked = buyersguide_factories.ProductPageFactory(parent=self.bg)
        # Link product pages to category
        buyersguide_factories.ProductPageCategoryFactory(product=product_page_live, category=category)
        buyersguide_factories.ProductPageCategoryFactory(product=product_page_not_live, category=category)

        products = category.published_product_pages

        self.assertIn(product_page_live, products)
        self.assertNotIn(product_page_not_live, products)
        self.assertNotIn(product_page_not_linked, products)
        self.assertEqual(category.published_product_page_count, 1)

        # Translate the category:
        self.translate_snippet(category, self.fr_locale)
        fr_category = category.get_translation(self.fr_locale)

        self.assertTrue(fr_category.is_being_used)

        # Check if the translated category has the same number of published product pages
        products = fr_category.published_product_pages

        # Even though the live product page is in English, it should still count
        self.assertEqual(fr_category.published_product_page_count, 1)
        self.assertIn(product_page_live, products)
        self.assertNotIn(product_page_not_live, products)
        self.assertNotIn(product_page_not_linked, products)

        # Translate the live page:
        self.translate_page(product_page_live, self.fr_locale)
        fr_product_page_live = product_page_live.get_translation(self.fr_locale)

        # Check if the translated category has the same number of published product pages
        del fr_category.published_product_pages  # Clear the cached property
        products = fr_category.published_product_pages

        # Even though we now have the English and French versions of the live page,
        # only the French one should count towards the number of published pages
        self.assertIn(fr_product_page_live, products)
        self.assertNotIn(product_page_live, products)
        self.assertEqual(fr_category.published_product_page_count, 1)

    def test_published_product_page_count_with_prefetching(self):
        BuyersGuideProductCategory.objects.all().delete()

        # Create product pages
        valid_product_pages = []
        for _ in range(20):
            valid_product_pages.append(buyersguide_factories.ProductPageFactory(live=True, parent=self.bg))
        product_page_not_live = buyersguide_factories.ProductPageFactory(live=False, parent=self.bg)
        product_page_not_linked = buyersguide_factories.ProductPageFactory(parent=self.bg)

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


class TestIsBeingUsedProperty(BuyersGuideTestCase):
    def setUp(self):
        super().setUp()
        self.admin_user = self.create_superuser(username="admin", password="password")
        self.login(self.admin_user)

    def test_usage_property_with_empty_category(self):
        BuyersGuideProductCategory.objects.all().delete()

        # Create category
        category = buyersguide_factories.BuyersGuideProductCategoryFactory()
        self.assertFalse(category.is_being_used)

        # Add a non-published page to the category
        buyersguide_factories.ProductPageCategoryFactory(
            product__live=False, product__parent=self.bg, category=category
        )
        del category.is_being_used  # Clear the cached property
        self.assertFalse(category.is_being_used)

        # Add a live page to the category
        buyersguide_factories.ProductPageCategoryFactory(
            product__live=True, product__parent=self.bg, category=category
        )
        # Now the category is being used
        del category.is_being_used  # Clear the cached property
        self.assertTrue(category.is_being_used)

    def test_usage_property_with_translated_pages(self):
        # Create category
        category = buyersguide_factories.BuyersGuideProductCategoryFactory()
        # Create product pages
        product_page_live = buyersguide_factories.ProductPageFactory(live=True, parent=self.bg)
        product_page_not_live = buyersguide_factories.ProductPageFactory(live=False, parent=self.bg)
        product_page_not_linked = buyersguide_factories.ProductPageFactory(parent=self.bg)
        # Link product pages to category
        buyersguide_factories.ProductPageCategoryFactory(product=product_page_live, category=category)
        buyersguide_factories.ProductPageCategoryFactory(product=product_page_not_live, category=category)

        self.assertTrue(category.is_being_used)

        # Translate the category:
        self.translate_snippet(category, self.fr_locale)
        fr_category = category.get_translation(self.fr_locale)
        self.assertTrue(fr_category.is_being_used)

        # Translate the live page:
        self.translate_page(product_page_live, self.fr_locale)
        self.assertTrue(fr_category.is_being_used)

    def test_usage_property_with_prefetching(self):
        BuyersGuideProductCategory.objects.all().delete()

        # Create product pages
        valid_product_pages = []
        for _ in range(20):
            valid_product_pages.append(buyersguide_factories.ProductPageFactory(live=True, parent=self.bg))
        product_page_not_live = buyersguide_factories.ProductPageFactory(live=False, parent=self.bg)
        product_page_not_linked = buyersguide_factories.ProductPageFactory(parent=self.bg)

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
                self.assertTrue(category.is_being_used)
