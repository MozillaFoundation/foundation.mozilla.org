from networkapi.wagtailpages.factory.libraries.rcc import (
    author_index as author_index_factory,
)
from networkapi.wagtailpages.factory.libraries.rcc import (
    detail_page as detail_page_factory,
)
from networkapi.wagtailpages.factory.libraries.rcc import (
    landing_page as landing_page_factory,
)
from networkapi.wagtailpages.factory.libraries.rcc import (
    library_page as library_page_factory,
)
from networkapi.wagtailpages.tests import base as test_base
from networkapi.wagtailpages.tests.libraries.rcc import utils


class RCCTestCase(test_base.WagtailpagesTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls._setup_rcc_structure(homepage=cls.homepage)

    @classmethod
    def _setup_rcc_structure(cls, homepage):
        cls.landing_page = landing_page_factory.RCCLandingPageFactory(
            parent=homepage,
            title="RCC Playbook",
            aside_cta__0="cta",
            aside_cta__1="cta",
        )
        cls.library_page = library_page_factory.RCCLibraryPageFactory(
            parent=cls.landing_page,
        )
        cls.author_index = author_index_factory.RCCAuthorsIndexPageFactory(
            parent=cls.landing_page,
            title="Browse Authors",
        )

    @staticmethod
    def create_rcc_detail_page_on_parent(*, parent, days_ago=0):
        publication_date = utils.days_ago(n=days_ago)
        return detail_page_factory.RCCDetailPageFactory(
            parent=parent,
            original_publication_date=publication_date,
        )

    @staticmethod
    def make_page_private(page):
        utils.make_page_private(page)

    def create_rcc_detail_page(self, days_ago=0):
        return self.create_rcc_detail_page_on_parent(
            parent=self.library_page,
            days_ago=days_ago,
        )

    def setUp(self):
        super().setUp()
        self.synchronize_tree()
