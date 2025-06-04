from foundation_cms.legacy_apps.wagtailpages.factory import (
    buyersguide as buyersguide_factories,
)
from foundation_cms.legacy_apps.wagtailpages.pagemodels.buyersguide.products import (
    BuyersGuideProductCategory,
    ProductPage,
)
from foundation_cms.legacy_apps.wagtailpages.pagemodels.buyersguide.utils import (
    _localize_category_parent,
    annotate_product_categories_local_names,
    get_buyersguide_featured_cta,
)
from foundation_cms.legacy_apps.wagtailpages.tests import base as test_base
from foundation_cms.legacy_apps.wagtailpages.tests.buyersguide import (
    base as bg_test_base,
)


class TestGetFeaturedCallToActionFunction(test_base.WagtailpagesTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.pni_homepage = buyersguide_factories.BuyersGuidePageFactory(
            parent=cls.homepage,
        )
        cls.content_index = buyersguide_factories.BuyersGuideEditorialContentIndexPageFactory(
            parent=cls.pni_homepage,
        )
        cls.product_page = buyersguide_factories.ProductPageFactory(
            parent=cls.pni_homepage,
        )

    def test_with_product_page(self):
        cta = buyersguide_factories.BuyersGuideCallToActionFactory()
        self.pni_homepage.call_to_action = cta
        self.pni_homepage.save()

        featured_cta = get_buyersguide_featured_cta(self.product_page)
        self.assertEqual(cta, featured_cta)

    def test_with_product_page_and_no_cta(self):
        self.pni_homepage.call_to_action = None
        self.pni_homepage.save()

        featured_cta = get_buyersguide_featured_cta(self.product_page)
        self.assertIsNone(featured_cta)

    def test_with_editorial_index_page(self):
        cta = buyersguide_factories.BuyersGuideCallToActionFactory()
        self.pni_homepage.call_to_action = cta
        self.pni_homepage.save()

        featured_cta = get_buyersguide_featured_cta(self.content_index)
        self.assertEqual(cta, featured_cta)

    def test_with_editorial_index_page_and_no_cta(self):
        self.pni_homepage.call_to_action = None
        self.pni_homepage.save()

        featured_cta = get_buyersguide_featured_cta(self.content_index)
        self.assertIsNone(featured_cta)

    def test_with_buyers_guide_home_page(self):
        cta = buyersguide_factories.BuyersGuideCallToActionFactory()
        self.pni_homepage.call_to_action = cta
        self.pni_homepage.save()

        featured_cta = get_buyersguide_featured_cta(self.pni_homepage)
        self.assertEqual(cta, featured_cta)

    def test_with_buyers_guide_home_page_and_no_cta(self):
        self.pni_homepage.call_to_action = None
        self.pni_homepage.save()

        featured_cta = get_buyersguide_featured_cta(self.pni_homepage)
        self.assertIsNone(featured_cta)


class LocalizeCategoryParentTests(test_base.WagtailpagesTestCase):
    def setUp(self):
        super().setUp()
        self.user = self.login()

    def test_can_localize_categories(self):
        # Create some categories
        parent_a = buyersguide_factories.BuyersGuideProductCategoryFactory()
        subcategory_a1 = buyersguide_factories.BuyersGuideProductCategoryFactory(
            parent=parent_a,
        )

        parent_b = buyersguide_factories.BuyersGuideProductCategoryFactory()
        subcategory_b1 = buyersguide_factories.BuyersGuideProductCategoryFactory(
            parent=parent_b,
        )
        subcategory_b2 = buyersguide_factories.BuyersGuideProductCategoryFactory(
            parent=parent_b,
        )

        category_no_parent = buyersguide_factories.BuyersGuideProductCategoryFactory()

        # Copy snippets for translation:
        self.translate_snippet(parent_a, self.fr_locale)
        fr_parent_a = parent_a.get_translation(self.fr_locale)
        self.translate_snippet(subcategory_a1, self.fr_locale)
        fr_subcategory_a1 = subcategory_a1.get_translation(self.fr_locale)
        self.translate_snippet(subcategory_b1, self.fr_locale)
        fr_subcategory_b1 = subcategory_b1.get_translation(self.fr_locale)

        # Make sure we can localize the parent of a category
        category_ids = [
            fr_parent_a.pk,
            fr_subcategory_a1.pk,
            parent_b.pk,
            fr_subcategory_b1.pk,
            subcategory_b2.pk,
            category_no_parent.pk,
        ]
        categories = BuyersGuideProductCategory.objects.filter(id__in=category_ids).select_related("parent").all()
        self.activate_locale(self.fr_locale)

        num_queries = 2 + 1  # 2 queries in the function + 1 to get the categories
        with self.assertNumQueries(num_queries):
            categories = _localize_category_parent(categories)

        categories_cache = {category.pk: category for category in categories}
        # Make sure parents are correct
        # Those that have local parents should have the local parent set up:
        fr_subcategory_a1 = categories_cache.get(fr_subcategory_a1.pk)
        self.assertEqual(fr_subcategory_a1.parent.pk, fr_parent_a.pk)

        # Those that did not have a local parent, should keep the default ones:
        fr_subcategory_b1 = categories_cache.get(fr_subcategory_b1.pk)
        self.assertEqual(fr_subcategory_b1.parent.pk, parent_b.pk)
        subcategory_b2 = categories_cache.get(subcategory_b2.pk)
        self.assertEqual(subcategory_b2.parent, parent_b)

        # Those that originally didn't have a parent, should continue to not have one
        # after localization:
        fr_parent_a = categories_cache.get(fr_parent_a.pk)
        self.assertIsNone(fr_parent_a.parent)
        parent_b = categories_cache.get(parent_b.pk)
        self.assertIsNone(parent_b.parent)
        category_no_parent = categories_cache.get(category_no_parent.pk)
        self.assertIsNone(category_no_parent.parent)


class AnnotateProductCategoriesLocalNamesTests(bg_test_base.BuyersGuideTestCase):
    def setUp(self):
        super().setUp()
        self.user = self.login()

    def test_can_annotate_local_names(self):
        # Create a product:
        product = buyersguide_factories.ProductPageFactory(
            parent=self.bg,
        )

        # Create some categories
        category_1 = buyersguide_factories.BuyersGuideProductCategoryFactory(name="Category 1")
        category_2 = buyersguide_factories.BuyersGuideProductCategoryFactory(name="Category 2")
        category_3 = buyersguide_factories.BuyersGuideProductCategoryFactory(name="Category 3")

        # Link the product to the categories:
        buyersguide_factories.ProductPageCategoryFactory(product=product, category=category_1)
        buyersguide_factories.ProductPageCategoryFactory(product=product, category=category_2)
        buyersguide_factories.ProductPageCategoryFactory(product=product, category=category_3)

        # Copy product/categories for translation:
        self.translate_page(product, self.fr_locale)
        fr_product = product.get_translation(self.fr_locale)
        self.translate_snippet(category_1, self.fr_locale)
        fr_category_1 = category_1.get_translation(self.fr_locale)
        fr_category_1.name = "Catégorie 1"
        fr_category_1.save()
        self.translate_snippet(category_2, self.fr_locale)
        fr_category_2 = category_2.get_translation(self.fr_locale)
        fr_category_2.name = "Catégorie 2"
        fr_category_2.save()

        product_ids = [fr_product.pk]
        products = ProductPage.objects.filter(id__in=product_ids).prefetch_related("product_categories__category")
        self.activate_locale(self.fr_locale)

        num_queries = 1 + 3  # 1 queries in the function + 3 to get the products
        with self.assertNumQueries(num_queries):
            products = annotate_product_categories_local_names(products, self.fr_locale.language_code)

        products_cache = {product.pk: product for product in products}
        # Make sure local names are correct
        fr_product = products_cache.get(fr_product.pk)
        self.assertEqual(fr_product.local_category_names, ["Catégorie 1", "Catégorie 2", "Category 3"])
