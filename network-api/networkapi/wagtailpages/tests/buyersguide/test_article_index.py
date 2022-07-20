from wagtail.tests import utils as wagtail_test

from networkapi.wagtailpages import models as pagemodels


class BuyersGuideArticleIndexPageTest(wagtail_test.WagtailPageTests):
    def test_parents(self):
        self.assertAllowedParentPageTypes(
            child_model=pagemodels.BuyersGuideEditorialContentIndexPage,
            parent_models={ pagemodels.BuyersGuidePage },
        )

    def test_children(self):
        self.assertAllowedSubpageTypes(
            parent_model=pagemodels.BuyersGuideEditorialContentIndexPage,
            child_models={ pagemodels.BuyersGuideArticlePage },
        )
