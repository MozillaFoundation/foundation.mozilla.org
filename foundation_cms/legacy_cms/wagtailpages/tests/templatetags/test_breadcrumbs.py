from foundation_cms.legacy_cms.wagtailpages.factory import profiles as profiles_factory
from foundation_cms.legacy_cms.wagtailpages.factory.libraries.rcc import (
    detail_page as rcc_detail_page_factory,
)
from foundation_cms.legacy_cms.wagtailpages.factory.libraries.rcc import (
    relations as rcc_relations_factory,
)
from foundation_cms.legacy_cms.wagtailpages.factory.libraries.research_hub import (
    detail_page as rh_detail_page_factory,
)
from foundation_cms.legacy_cms.wagtailpages.factory.libraries.research_hub import (
    relations as rh_relations_factory,
)
from foundation_cms.legacy_cms.wagtailpages.templatetags import (
    breadcrumbs as breadcrumbs_tags,
)
from foundation_cms.legacy_cms.wagtailpages.tests.libraries.rcc.base import RCCTestCase
from foundation_cms.legacy_cms.wagtailpages.tests.libraries.research_hub.base import (
    ResearchHubTestCase,
)


class TestGetResearchBreadcrumb(ResearchHubTestCase):
    def test_author_index_breadcrumbs(self):
        request = self.client.get(self.author_index.url)
        breadcrumbs = breadcrumbs_tags.research_breadcrumbs(request.context)["breadcrumb_list"]
        # Author Index page should only have 1 breadcrumb, "Research"
        expected_breadcrumbs = [{"title": "Research", "url": "/en/research/"}]
        self.assertEqual(len(breadcrumbs), 1)
        self.assertEqual(breadcrumbs, expected_breadcrumbs)

    def test_author_detail_breadcrumbs_override(self):
        detail_page = self.create_research_detail_page_on_parent(parent=self.library_page, days_ago=14)
        research_profile = profiles_factory.ProfileFactory()
        research_profile.refresh_from_db()
        rh_relations_factory.ResearchAuthorRelationFactory(
            detail_page=detail_page,
            author_profile=research_profile,
        )

        profile_url = self.author_index.reverse_subpage(
            "research-author-detail",
            kwargs={"profile_slug": research_profile.slug},
        )

        request = self.client.get(self.author_index.url + profile_url)

        breadcrumbs = breadcrumbs_tags.research_breadcrumbs(request.context, include_self=True)["breadcrumb_list"]
        # Author Detail page should have 2 breadcrumbs, "Research/Authors"
        expected_breadcrumbs = [
            {"title": "Research", "url": "/en/research/"},
            {"title": "Authors", "url": "/en/research/authors/"},
        ]

        self.assertEqual(len(breadcrumbs), 2)
        self.assertEqual(breadcrumbs, expected_breadcrumbs)

    def test_research_detail_page_breadcrumbs(self) -> None:
        detail_page = rh_detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
        )
        response = self.client.get(detail_page.url)
        breadcrumbs = breadcrumbs_tags.research_breadcrumbs(response.context)["breadcrumb_list"]
        expected_breadcrumbs = [
            {"title": "Research", "url": "/en/research/"},
            {"title": "Library", "url": "/en/research/library/"},
        ]

        self.assertEqual(len(breadcrumbs), 2)
        self.assertEqual(breadcrumbs, expected_breadcrumbs)

    def test_library_page_breadcrumbs(self):
        response = self.client.get(self.library_page.url)
        breadcrumbs = breadcrumbs_tags.research_breadcrumbs(response.context)["breadcrumb_list"]
        expected_breadcrumbs = [{"title": "Research", "url": "/en/research/"}]

        self.assertEqual(len(breadcrumbs), 1)
        self.assertEqual(breadcrumbs, expected_breadcrumbs)


class TestGetRCCBreadcrumb(RCCTestCase):
    def test_author_index_breadcrumbs(self):
        request = self.client.get(self.author_index.url)
        breadcrumbs = breadcrumbs_tags.rcc_breadcrumbs(request.context)["breadcrumb_list"]
        # Author Index page should only have 1 breadcrumb, "RCC Playbook"
        expected_breadcrumbs = [{"title": "RCC Playbook", "url": "/en/rcc-playbook/"}]
        self.assertEqual(len(breadcrumbs), 1)
        self.assertEqual(breadcrumbs, expected_breadcrumbs)

    def test_author_detail_breadcrumbs_override(self):
        detail_page = self.create_rcc_detail_page_on_parent(parent=self.library_page, days_ago=14)
        research_profile = profiles_factory.ProfileFactory()
        research_profile.refresh_from_db()
        rcc_relations_factory.RCCAuthorRelationFactory(
            detail_page=detail_page,
            author_profile=research_profile,
        )

        profile_url = self.author_index.reverse_subpage(
            "rcc-author-detail",
            kwargs={"profile_slug": research_profile.slug},
        )

        request = self.client.get(self.author_index.url + profile_url)

        breadcrumbs = breadcrumbs_tags.rcc_breadcrumbs(request.context, include_self=True)["breadcrumb_list"]
        # Author Detail page should have 2 breadcrumbs, "Research/Authors"
        expected_breadcrumbs = [
            {"title": "RCC Playbook", "url": "/en/rcc-playbook/"},
            {"title": "Browse Authors", "url": "/en/rcc-playbook/browse-authors/"},
        ]

        self.assertEqual(len(breadcrumbs), 2)
        self.assertEqual(breadcrumbs, expected_breadcrumbs)

    def test_rcc_detail_page_breadcrumbs(self) -> None:
        detail_page = rcc_detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
        )
        response = self.client.get(detail_page.url)
        breadcrumbs = breadcrumbs_tags.rcc_breadcrumbs(response.context)["breadcrumb_list"]
        expected_breadcrumbs = [
            {"title": "RCC Playbook", "url": "/en/rcc-playbook/"},
            {"title": "Curriculum Library", "url": "/en/rcc-playbook/curriculum-library/"},
        ]

        self.assertEqual(len(breadcrumbs), 2)
        self.assertEqual(breadcrumbs, expected_breadcrumbs)

    def test_library_page_breadcrumbs(self):
        response = self.client.get(self.library_page.url)
        breadcrumbs = breadcrumbs_tags.rcc_breadcrumbs(response.context)["breadcrumb_list"]
        expected_breadcrumbs = [{"title": "RCC Playbook", "url": "/en/rcc-playbook/"}]

        self.assertEqual(len(breadcrumbs), 1)
        self.assertEqual(breadcrumbs, expected_breadcrumbs)
