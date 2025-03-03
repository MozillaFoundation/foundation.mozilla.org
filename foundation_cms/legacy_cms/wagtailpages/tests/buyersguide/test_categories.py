from foundation_cms.legacy_cms.wagtailpages.factory import buyersguide as buyersguide_factories
from foundation_cms.legacy_cms.wagtailpages.pagemodels.buyersguide.products import (
    BuyersGuideProductCategory,
)
from foundation_cms.legacy_cms.wagtailpages.tests.buyersguide.base import BuyersGuideTestCase


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
        # Link product pages to category
        buyersguide_factories.ProductPageCategoryFactory(product=product_page_live, category=category)

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

        for _ in range(5):
            # Create category
            category = buyersguide_factories.BuyersGuideProductCategoryFactory()
            # Link product pages to category
            for product_page in valid_product_pages:
                buyersguide_factories.ProductPageCategoryFactory(product=product_page, category=category)

        query_number = 1
        with self.assertNumQueries(query_number):
            categories = BuyersGuideProductCategory.objects.all().with_usage_annotation()
            for category in categories:
                self.assertTrue(category.is_being_used)

    def test_created_categories_get_slug(self):
        category = buyersguide_factories.BuyersGuideProductCategoryFactory()
        self.assertTrue(category.slug)
        category = buyersguide_factories.BuyersGuideProductCategoryFactory(name="Test Category")
        self.assertEqual(category.slug, "test-category")

    def test_localized_categories_sync_slugs(self):
        category = buyersguide_factories.BuyersGuideProductCategoryFactory()
        self.assertTrue(category.slug)

        self.translate_snippet(category, self.fr_locale)
        fr_category = category.get_translation(self.fr_locale)

        self.assertEqual(fr_category.slug, category.slug)
