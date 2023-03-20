from networkapi.wagtailpages.factory.research_hub import author_index as author_index_factory
from networkapi.wagtailpages.factory.research_hub import landing_page as landing_page_factory
from networkapi.wagtailpages.factory.research_hub import library_page as library_page_factory
from networkapi.wagtailpages.tests import base as test_base


class ResearchHubTestCase(test_base.WagtailpagesTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls._setup_research_hub_structure(homepage=cls.homepage)

    @classmethod
    def _setup_research_hub_structure(cls, homepage):
        cls.landing_page = landing_page_factory.ResearchLandingPageFactory(
            parent=homepage,
        )
        cls.library_page = library_page_factory.ResearchLibraryPageFactory(
            parent=cls.landing_page,
        )
        cls.author_index = author_index_factory.ResearchAuthorsIndexPageFactory(
            parent=cls.landing_page,
            title="Authors",
        )

    def setUp(self):
        self.synchronize_tree()
