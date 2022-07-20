from wagtail.tests import utils as wagtail_test

from networkapi.wagtailpages import models as pagemodels
from networkapi.wagtailpages.factory import buyersguide as buyersguide_factories


class BuyersGuideArticlePageFactoryTest(wagtail_test.WagtailPageTests):
    def test_factory(self):
        buyersguide_factories.BuyersGuideArticlePageFactory()


class BuyersGuideArticlePageTest(wagtail_test.WagtailPageTests):
    def test_parents(self):
        self.assertAllowedParentPageTypes(
            child_model=pagemodels.BuyersGuideArticlePage,
            parent_models={pagemodels.BuyersGuideEditorialContentIndexPage},
        )
