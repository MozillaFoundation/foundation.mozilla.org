from networkapi.wagtailpages.factory import research_hub as research_factory
from networkapi.wagtailpages.tests import base as test_base


class ResearchHubTestCase(test_base.WagtailpagesTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls._setup_research_hub_structure(homepage=cls.homepage)

    @classmethod
    def _setup_research_hub_structure(cls, homepage):
        cls.landing_page = research_factory.ResearchLandingPageFactory(
            parent=homepage,
        )
        cls.library_page = research_factory.ResearchLibraryPageFactory(
            parent=cls.landing_page,
        )
        cls.author_index = research_factory.ResearchAuthorsIndexPageFactory(
            parent=cls.landing_page,
            title='Authors',
        )

    def setUp(self):
        self.synchronize_tree()
