from django.core import exceptions

from networkapi.wagtailpages.factory import buyersguide as buyersguide_factories
from networkapi.wagtailpages.tests import base as test_base


class TestBuyersGuideContentCategory(test_base.WagtailpagesTestCase):
    def test_factory(self):
        buyersguide_factories.BuyersGuideContentCategoryFactory()

    def test_slug_set_during_save(self):
        category = buyersguide_factories.BuyersGuideContentCategoryFactory.build(
            title="Test category",
        )
        self.assertEqual(category.slug, "")

        category.save()

        self.assertEqual(category.slug, "en-test-category")

    def test_exisiting_slug_is_not_kept_during_save(self):
        category = buyersguide_factories.BuyersGuideContentCategoryFactory(
            title="Test category",
            slug="not-the-slugified-title",
        )

        category.save()

        self.assertEqual(category.title, "Test category")
        self.assertEqual(category.slug, "en-test-category")

    def test_slug_has_to_be_unique(self):
        buyersguide_factories.BuyersGuideContentCategoryFactory(
            title="Test category",
        )
        category = buyersguide_factories.BuyersGuideContentCategoryFactory.build(
            title="Test category",
        )

        with self.assertRaises(exceptions.ValidationError):
            category.full_clean()

    def test_slug_different_for_different_locales(self):
        category_default_locale = buyersguide_factories.BuyersGuideContentCategoryFactory(
            title="Test category",
        )
        category_fr_locale = buyersguide_factories.BuyersGuideContentCategoryFactory.build(
            title="Test category",
            locale=self.fr_locale,
        )

        category_fr_locale.save()

        self.assertEqual(category_fr_locale.title, category_default_locale.title)
        self.assertNotEqual(category_fr_locale.locale, category_default_locale.locale)
        self.assertNotEqual(category_fr_locale.slug, category_default_locale.slug)

    def test_copy_for_translation(self):
        category_default_locale = buyersguide_factories.BuyersGuideContentCategoryFactory(
            title="Test category",
        )

        fr_copy = category_default_locale.copy_for_translation(locale=self.fr_locale)

        fr_copy.full_clean()
        fr_copy.save()
