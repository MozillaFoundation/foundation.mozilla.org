from networkapi.wagtailpages.factory import buyersguide as buyersguide_factories
from networkapi.wagtailpages.pagemodels.buyersguide.utils import (
    get_buyersguide_featured_cta,
)
from networkapi.wagtailpages.tests import base as test_base


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
