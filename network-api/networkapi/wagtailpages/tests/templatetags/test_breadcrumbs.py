from networkapi.wagtailpages.factory import profiles as profiles_factory
from networkapi.wagtailpages.factory.research_hub import (
    detail_page as detail_page_factory,
)
from networkapi.wagtailpages.factory.research_hub import relations as relations_factory
from networkapi.wagtailpages.templatetags import breadcrumbs as breadcrumbs_tags
from networkapi.wagtailpages.tests.libraries.research_hub.base import ResearchHubTestCase


class TestGetResearchBreadcrumb(ResearchHubTestCase):
    def test_author_index_breadcrumbs(self):
        request = self.client.get(self.author_index.url)
        breadcrumbs = breadcrumbs_tags.get_research_breadcrumbs(request.context)["breadcrumb_list"]
        # Author Index page should only have 1 breadcrumb, "Research"
        expected_breadcrumbs = [{"title": "Research", "url": "/en/research/"}]
        self.assertEqual(len(breadcrumbs), 1)
        self.assertEqual(breadcrumbs, expected_breadcrumbs)

    def test_author_detail_breadcrumbs_override(self):
        detail_page = self.create_research_detail_page_on_parent(parent=self.library_page, days_ago=14)
        research_profile = profiles_factory.ProfileFactory()
        research_profile.refresh_from_db()
        relations_factory.ResearchAuthorRelationFactory(
            research_detail_page=detail_page,
            author_profile=research_profile,
        )

        profile_url = self.author_index.reverse_subpage(
            "wagtailpages:research-author-detail",
            kwargs={"profile_slug": research_profile.slug},
        )

        request = self.client.get(self.author_index.url + profile_url)

        breadcrumbs = breadcrumbs_tags.get_research_breadcrumbs(request.context, include_self=True)["breadcrumb_list"]
        # Author Detail page should have 2 breadcrumbs, "Research/Authors"
        expected_breadcrumbs = [
            {"title": "Research", "url": "/en/research/"},
            {"title": "Authors", "url": "/en/research/authors/"},
        ]

        self.assertEqual(len(breadcrumbs), 2)
        self.assertEqual(breadcrumbs, expected_breadcrumbs)

    def test_research_detail_page_breadcrumbs(self) -> None:
        detail_page = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
        )
        response = self.client.get(detail_page.url)
        breadcrumbs = breadcrumbs_tags.get_research_breadcrumbs(response.context)["breadcrumb_list"]
        expected_breadcrumbs = [
            {"title": "Research", "url": "/en/research/"},
            {"title": "Library", "url": "/en/research/library/"},
        ]

        self.assertEqual(len(breadcrumbs), 2)
        self.assertEqual(breadcrumbs, expected_breadcrumbs)

    def test_library_page_breadcrumbs(self):
        response = self.client.get(self.library_page.url)
        breadcrumbs = breadcrumbs_tags.get_research_breadcrumbs(response.context)["breadcrumb_list"]
        expected_breadcrumbs = [{"title": "Research", "url": "/en/research/"}]

        self.assertEqual(len(breadcrumbs), 1)
        self.assertEqual(breadcrumbs, expected_breadcrumbs)
