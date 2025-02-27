from django.core import exceptions

from legacy_cms.wagtailpages.factory import buyersguide as buyersguide_factories
from legacy_cms.wagtailpages.tests import base as test_base

TEST_CATEGORY_TITLE = "Test category"


class TestBuyersGuideContentCategory(test_base.WagtailpagesTestCase):
    def test_factory(self):
        buyersguide_factories.BuyersGuideContentCategoryFactory()

    def test_factory_sets_slug(self):
        category = buyersguide_factories.BuyersGuideContentCategoryFactory.build(
            title=TEST_CATEGORY_TITLE,
        )
        self.assertEqual(category.slug, "test-category")

    def test_full_clean_raises_if_category_with_same_title_and_locale_in_db(self):
        buyersguide_factories.BuyersGuideContentCategoryFactory(
            title=TEST_CATEGORY_TITLE,
        )
        category = buyersguide_factories.BuyersGuideContentCategoryFactory.build(
            title=TEST_CATEGORY_TITLE,
        )

        with self.assertRaises(exceptions.ValidationError):
            category.full_clean()

    def test_can_clean_and_save_copy_for_translation(self):
        category_default_locale = buyersguide_factories.BuyersGuideContentCategoryFactory(
            title=TEST_CATEGORY_TITLE,
        )

        fr_copy = category_default_locale.copy_for_translation(locale=self.fr_locale)
        fr_copy.full_clean()
        fr_copy.save()

        self.assertEqual(category_default_locale.slug, "test-category")
        self.assertEqual(fr_copy.slug, "test-category")
