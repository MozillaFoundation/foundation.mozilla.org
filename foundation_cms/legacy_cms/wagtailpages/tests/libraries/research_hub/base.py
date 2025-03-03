from foundation_cms.legacy_cms.wagtailpages.factory.libraries.research_hub import (
    author_index as author_index_factory,
)
from foundation_cms.legacy_cms.wagtailpages.factory.libraries.research_hub import (
    detail_page as detail_page_factory,
)
from foundation_cms.legacy_cms.wagtailpages.factory.libraries.research_hub import (
    landing_page as landing_page_factory,
)
from foundation_cms.legacy_cms.wagtailpages.factory.libraries.research_hub import (
    library_page as library_page_factory,
)
from foundation_cms.legacy_cms.wagtailpages.tests import base as test_base
from foundation_cms.legacy_cms.wagtailpages.tests.libraries.research_hub import utils


class ResearchHubTestCase(test_base.WagtailpagesTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls._setup_research_hub_structure(homepage=cls.homepage)

    @classmethod
    def _setup_research_hub_structure(cls, homepage):
        cls.landing_page = landing_page_factory.ResearchLandingPageFactory(
            parent=homepage,
            aside_cta__0="cta",
            aside_cta__1="cta",
        )
        cls.library_page = library_page_factory.ResearchLibraryPageFactory(
            parent=cls.landing_page,
        )
        cls.author_index = author_index_factory.ResearchAuthorsIndexPageFactory(
            parent=cls.landing_page,
            title="Authors",
        )

    @staticmethod
    def create_research_detail_page_on_parent(*, parent, days_ago=0):
        publication_date = utils.days_ago(n=days_ago)
        return detail_page_factory.ResearchDetailPageFactory(
            parent=parent,
            original_publication_date=publication_date,
        )

    @staticmethod
    def make_page_private(page):
        utils.make_page_private(page)

    def create_research_detail_page(self, days_ago=0):
        return self.create_research_detail_page_on_parent(
            parent=self.library_page,
            days_ago=days_ago,
        )

    def setUp(self):
        super().setUp()
        self.synchronize_tree()
        self.activate_locale(self.default_locale)
