from django import db
from networkapi.wagtailpages.tests import base as test_base
from networkapi.wagtailpages.factory import buyersguide as buyersguide_factories


class TestBuyersGuideContentCategory(test_base.WagtailpagesTestCase):
    def test_factory(self):
        buyersguide_factories.BuyersGuideContentCategoryFactory()

    def test_slug_set_during_save(self):
        category = buyersguide_factories.BuyersGuideContentCategoryFactory.build()
        self.assertEqual(category.slug, '')

        category.save()

        self.assertNotEqual(category.slug, '')

    def test_exisiting_slug_is_kept_during_save(self):
        category = buyersguide_factories.BuyersGuideContentCategoryFactory(
            title='Test category',
            slug='not-the-slugified-title',
        )

        category.save()

        self.assertEqual(category.title, 'Test category')
        self.assertEqual(category.slug, 'not-the-slugified-title')

    def test_slug_has_to_be_unique(self):
        buyersguide_factories.BuyersGuideContentCategoryFactory(
            title='Test category',
            slug='test-category',
        )
        category = buyersguide_factories.BuyersGuideContentCategoryFactory.build(
            title='Test category',
            slug='test-category',
        )

        with self.assertRaises(db.IntegrityError) as _:
            category.save()

    def test_same_slug_allowed_on_different_locale(self):
        category_default_locale = buyersguide_factories.BuyersGuideContentCategoryFactory(
            title='Test category',
            slug='test-category',
            locale=self.default_locale,
        )
        category_fr_locale = buyersguide_factories.BuyersGuideContentCategoryFactory.build(
            title='Test category',
            slug='test-category',
            locale=self.fr_locale,
        )

        category_fr_locale.save()

        self.assertEqual(category_fr_locale.slug, category_default_locale.slug)
        self.assertNotEqual(category_fr_locale.locale, category_default_locale.locale)



