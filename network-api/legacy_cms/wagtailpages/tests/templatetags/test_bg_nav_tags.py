from wagtail.models import Locale

from legacy_cms.wagtailpages.factory import buyersguide as buyersguide_factories
from legacy_cms.wagtailpages.templatetags.bg_nav_tags import bg_categories_in_subnav
from legacy_cms.wagtailpages.tests.buyersguide.base import BuyersGuideTestCase


class TestBgCategoriesInSubnav(BuyersGuideTestCase):
    def setUp(self):
        super().setUp()
        self.login()

    def test_correct_categories_returned(self):
        # Create categories
        cat_a = buyersguide_factories.BuyersGuideProductCategoryFactory()
        cat_b = buyersguide_factories.BuyersGuideProductCategoryFactory()
        cat_c = buyersguide_factories.BuyersGuideProductCategoryFactory()
        cat_not_in_nav = buyersguide_factories.BuyersGuideProductCategoryFactory()
        # Link categories to navbar
        buyersguide_factories.BuyersGuideCategoryNavRelationFactory(category=cat_a, sort_order=3)
        buyersguide_factories.BuyersGuideCategoryNavRelationFactory(category=cat_b, sort_order=2)
        buyersguide_factories.BuyersGuideCategoryNavRelationFactory(category=cat_c, sort_order=1)

        # Get categories in subnav
        categories_in_subnav = bg_categories_in_subnav()
        self.assertEqual(len(categories_in_subnav), 3)

        # Check that the categories are in the correct sort order (c, b, a)
        self.assertCountEqual([cat_c, cat_b, cat_a], list(categories_in_subnav))

        # Check that the category not selected is not in the subnav
        self.assertNotIn(cat_not_in_nav, categories_in_subnav)

    def test_categories_returned_in_correct_locale(self):
        # Create categories
        cat_a = buyersguide_factories.BuyersGuideProductCategoryFactory()
        cat_b = buyersguide_factories.BuyersGuideProductCategoryFactory()
        cat_c = buyersguide_factories.BuyersGuideProductCategoryFactory()
        # Link categories to navbar
        buyersguide_factories.BuyersGuideCategoryNavRelationFactory(category=cat_a, sort_order=3)
        buyersguide_factories.BuyersGuideCategoryNavRelationFactory(category=cat_b, sort_order=2)
        buyersguide_factories.BuyersGuideCategoryNavRelationFactory(category=cat_c, sort_order=1)

        # Get categories in subnav
        categories_in_subnav = bg_categories_in_subnav()
        self.assertEqual(len(categories_in_subnav), 3)

        # Check that the categories are in the correct sort order (c, b, a)
        self.assertCountEqual([cat_c, cat_b, cat_a], list(categories_in_subnav))

        # Translate the categories (only cat_a and cat_b, cat_c should default to English)
        self.translate_snippet(cat_a, self.fr_locale)
        self.translate_snippet(cat_b, self.fr_locale)
        cat_a_fr = cat_a.get_translation(self.fr_locale)
        cat_a_fr.name = "[FR]" + cat_a_fr.name
        cat_a_fr.save()
        cat_b_fr = cat_b.get_translation(self.fr_locale)
        cat_b_fr.name = "[FR]" + cat_b_fr.name
        cat_b_fr.save()

        # Activate the French locale
        self.activate_locale(self.fr_locale)
        self.assertEqual(Locale.get_active(), self.fr_locale)

        # Get categories in subnav
        fr_categories_in_subnav = bg_categories_in_subnav()

        # Check that the categories are in the correct sort order (c, b, a) and contain
        # the local versions where available
        self.assertCountEqual([cat_c, cat_b_fr, cat_a_fr], list(fr_categories_in_subnav))

        # Check that default versions are not displayed if they have a local version
        self.assertNotIn(cat_a, fr_categories_in_subnav)
        self.assertNotIn(cat_b, fr_categories_in_subnav)
