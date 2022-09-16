from networkapi.wagtailpages.factory import buyersguide as buyersguide_factories
from networkapi.wagtailpages.pagemodels.buyersguide.utils import get_bg_featured_cta
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

    def test_get_bg_featured_cta_with_product_page(self):
        self.pni_homepage.call_to_action = buyersguide_factories.BuyersGuideCallToActionFactory()
        self.pni_homepage.save()

        featured_cta = get_bg_featured_cta(self.product_page)
        self.assertIsNotNone(featured_cta)

    def test_get_bg_featured_cta_with_editorial_index_page(self):
        self.pni_homepage.call_to_action = buyersguide_factories.BuyersGuideCallToActionFactory()
        self.pni_homepage.save()

        featured_cta = get_bg_featured_cta(self.content_index)
        self.assertIsNotNone(featured_cta)

    def test_get_bg_featured_cta_with_bg_home_page(self):
        self.pni_homepage.call_to_action = buyersguide_factories.BuyersGuideCallToActionFactory()
        self.pni_homepage.save()

        featured_cta = get_bg_featured_cta(self.pni_homepage)
        self.assertIsNotNone(featured_cta)

    def test_get_bg_featured_cta_with_no_cta_set(self):
        self.pni_homepage.call_to_action = None
        self.pni_homepage.save()

        featured_cta = get_bg_featured_cta(self.content_index)
        self.assertIsNone(featured_cta)
