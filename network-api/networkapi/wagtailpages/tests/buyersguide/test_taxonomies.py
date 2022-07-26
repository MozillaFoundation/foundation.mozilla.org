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
