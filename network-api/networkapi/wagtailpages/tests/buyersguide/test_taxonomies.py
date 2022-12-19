from django.core import exceptions

from networkapi.wagtailpages.factory import buyersguide as buyersguide_factories
from networkapi.wagtailpages.tests import base as test_base


class TestBuyersGuideContentCategory(test_base.WagtailpagesTestCase):
    def test_factory(self):
        buyersguide_factories.BuyersGuideContentCategoryFactory()

    def test_clean_sets_slug(self):
        category = buyersguide_factories.BuyersGuideContentCategoryFactory.build(
            title="Test category",
        )
        self.assertEqual(category.slug, "")

        category.clean()

        self.assertEqual(category.slug, "en-test-category")

    def test_clean_overrides_exisiting_slug(self):
        category = buyersguide_factories.BuyersGuideContentCategoryFactory.build(
            title="Test category",
            slug="not-the-slugified-title",
        )

        category.clean()

        self.assertEqual(category.title, "Test category")
        self.assertEqual(category.slug, "en-test-category")

    def test_clean_raises_if_category_with_same_title_and_locale_in_db(self):
        buyersguide_factories.BuyersGuideContentCategoryFactory(
            title="Test category",
        )
        category = buyersguide_factories.BuyersGuideContentCategoryFactory.build(
            title="Test category",
        )

        with self.assertRaises(exceptions.ValidationError):
            category.clean_slug()

    def test_clean_slug_different_for_different_locales(self):
        category_default_locale = buyersguide_factories.BuyersGuideContentCategoryFactory.build(
            title="Test category",
        )
        category_fr_locale = buyersguide_factories.BuyersGuideContentCategoryFactory.build(
            title="Test category",
            locale=self.fr_locale,
        )

        category_default_locale.clean_slug()
        category_fr_locale.clean_slug()

        self.assertEqual(category_fr_locale.title, category_default_locale.title)
        self.assertNotEqual(category_fr_locale.locale, category_default_locale.locale)
        self.assertNotEqual(category_fr_locale.slug, category_default_locale.slug)

    def test_can_clean_and_save_copy_for_translation(self):
        category_default_locale = buyersguide_factories.BuyersGuideContentCategoryFactory(
            title="Test category",
        )

        fr_copy = category_default_locale.copy_for_translation(locale=self.fr_locale)

        fr_copy.full_clean()
        fr_copy.save()
