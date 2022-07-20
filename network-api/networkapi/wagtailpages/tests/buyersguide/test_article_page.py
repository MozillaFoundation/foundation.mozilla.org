from wagtail.tests import utils as wagtail_test

from networkapi.wagtailpages import models as pagemodels


class BuyersGuideArticlePageTest(wagtail_test.WagtailPageTests):
    def test_parents(self):
        self.assertAllowedParentPageTypes(
            child_model=pagemodels.BuyersGuideArticlePage,
            parent_models={ pagemodels.BuyersGuideArticleIndexPage },
        )
