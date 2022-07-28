import unittest

from django.core import exceptions
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

        with self.assertRaises(exceptions.ValidationError):
            category.full_clean()

    @unittest.skip(
        'We would really want the slugs to be only unique per locale. '
        'If we implement that with a UniqueContraint or unique_together, '
        'Wagtail will crash if the constraint is violated. '
        'Wagtail does handle the simple unique requirement on the slug field gracefully. '
        'Therefore, we are using slugs that are unique regardless of locale. '
        'We need to manually create unique slugs if there are clashes between the locales. '
        'Because we are using slugs that need to be unique regradless of locale, this '
        'test would fail. Therefore it is skipped.'
        'See also: https://github.com/wagtail/wagtail/issues/8918'
    )
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

