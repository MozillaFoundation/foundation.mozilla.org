import wagtail_factories
from django.core import exceptions
from django.utils import translation

from networkapi.wagtailpages.factory.research_hub import (
    detail_page as detail_page_factory,
)
from networkapi.wagtailpages.factory.research_hub import relations as relations_factory
from networkapi.wagtailpages.models import (
    ArticlePage,
    PublicationPage,
    ResearchDetailPage,
)
from networkapi.wagtailpages.tests.research_hub import base as research_test_base
from networkapi.wagtailpages.tests.research_hub import utils as research_test_utils


class TestResearchLibraryDetailPage(research_test_base.ResearchHubTestCase):
    def test_children(self):
        self.assertAllowedSubpageTypes(
            parent_model=ResearchDetailPage,
            child_models={ArticlePage, PublicationPage},
        )

    def test_research_detail_page_breadcrumbs(self) -> None:
        detail_page = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
        )
        response = self.client.get(detail_page.url)
        breadcrumbs = response.context["breadcrumbs"]
        expected_breadcrumbs = [
            {"title": "Research", "url": "/en/research/"},
            {"title": "Library", "url": "/en/research/library/"},
        ]

        self.assertEqual(len(breadcrumbs), 2)
        self.assertEqual(breadcrumbs, expected_breadcrumbs)

    def test_get_research_authors(self) -> None:
        author_profiles = []
        detail_page = detail_page_factory.ResearchDetailPageFactory(parent=self.library_page, research_authors=[])

        for _ in range(3):
            research_author_relation = relations_factory.ResearchAuthorRelationFactory(
                research_detail_page=detail_page
            )
            author_profiles.append(research_author_relation.author_profile)

        research_authors = list(detail_page.get_research_authors())

        self.assertEqual(len(research_authors), 3)
        self.assertCountEqual(author_profiles, research_authors)

    def test_get_research_authors(self) -> None:
        """
        Testing that the get_research_authors method returns all research author profiles.
        """
        author_profiles = []
        detail_page = detail_page_factory.ResearchDetailPageFactory(parent=self.library_page, research_authors=[])

        for _ in range(3):
            research_author_relation = relations_factory.ResearchAuthorRelationFactory(
                research_detail_page=detail_page
            )
            author_profiles.append(research_author_relation.author_profile)

        research_authors = list(detail_page.get_research_authors())

        self.assertEqual(len(research_authors), 3)
        self.assertCountEqual(author_profiles, research_authors)

    def test_get_research_authors_returns_localized_profiles(self):
        """
        When a profile for the active locale exists, the get_research_authors method should return it.
        """
        detail_page = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
        )
        profile_en = detail_page.research_authors.first().author_profile
        self.synchronize_tree()
        detail_page_fr = research_test_utils.translate_detail_page(detail_page, self.fr_locale)
        profile_fr = detail_page_fr.research_authors.first().author_profile

        research_authors_en = detail_page.localized.get_research_authors()
        translation.activate(self.fr_locale.language_code)
        research_authors_fr = detail_page.localized.get_research_authors()

        self.assertEqual(len(research_authors_en), 1)
        self.assertEqual(len(research_authors_fr), 1)
        self.assertIn(profile_en, research_authors_en)
        self.assertNotIn(profile_fr, research_authors_en)
        self.assertIn(profile_fr, research_authors_fr)
        self.assertNotIn(profile_en, research_authors_fr)


class TestResearchDetailLink(research_test_base.ResearchHubTestCase):
    def test_clean_with_url(self) -> None:
        link = detail_page_factory.ResearchDetailLinkFactory.build(with_url=True)

        link.clean()

        self.assertTrue(link.url)
        self.assertFalse(link.page)
        self.assertFalse(link.document)

    def test_clean_with_page(self) -> None:
        link = detail_page_factory.ResearchDetailLinkFactory.build(with_page=True)

        link.clean()

        self.assertTrue(link.page)
        self.assertFalse(link.url)
        self.assertFalse(link.document)

    def test_clean_with_doc(self) -> None:
        link = detail_page_factory.ResearchDetailLinkFactory.build(with_document=True)

        link.clean()

        self.assertTrue(link.document)
        self.assertFalse(link.url)
        self.assertFalse(link.page)

    def test_clean_with_url_and_page(self) -> None:
        link = detail_page_factory.ResearchDetailLinkFactory.build(
            with_url=True,
            with_page=True,
        )

        with self.assertRaises(exceptions.ValidationError):
            link.clean()

    def test_clean_with_url_and_doc(self) -> None:
        link = detail_page_factory.ResearchDetailLinkFactory.build(
            with_url=True,
            with_document=True,
        )

        with self.assertRaises(exceptions.ValidationError):
            link.clean()

    def test_clean_with_page_and_doc(self) -> None:
        link = detail_page_factory.ResearchDetailLinkFactory.build(
            with_url=True,
            with_page=True,
        )

        with self.assertRaises(exceptions.ValidationError):
            link.clean()

    def test_clean_with_url_and_page_and_doc(self) -> None:
        link = detail_page_factory.ResearchDetailLinkFactory.build(
            with_url=True,
            with_page=True,
            with_document=True,
        )

        with self.assertRaises(exceptions.ValidationError):
            link.clean()

    def test_clean_with_neither_url_page_nor_doc(self):
        link = detail_page_factory.ResearchDetailLinkFactory.build()

        with self.assertRaises(exceptions.ValidationError):
            link.clean()

    def test_get_url_with_url(self) -> None:
        url = "https://example.com"
        link = detail_page_factory.ResearchDetailLinkFactory.build(url=url)

        self.assertEqual(link.get_url(), url)

    def test_get_url_with_page(self) -> None:
        page = wagtail_factories.PageFactory(parent=self.homepage)
        link = detail_page_factory.ResearchDetailLinkFactory.build(page=page)

        self.assertEqual(link.get_url(), page.get_url())

    def test_get_url_with_non_live_page(self) -> None:
        page = wagtail_factories.PageFactory(parent=self.homepage, live=False)
        link = detail_page_factory.ResearchDetailLinkFactory.build(page=page)

        self.assertEqual(link.get_url(), "")

    def test_get_url_with_doc(self) -> None:
        doc = wagtail_factories.DocumentFactory()
        link = detail_page_factory.ResearchDetailLinkFactory.build(document=doc)

        self.assertEqual(link.get_url(), doc.url)

    def test_get_url_without_needed_data(self) -> None:
        """
        Test the invalid link case.

        This link should raise a validation error when it is being created, but the `get_url` method still needs to
        handle this logic branch in a sensible manner.

        """
        link = detail_page_factory.ResearchDetailLinkFactory.build()

        with self.assertRaises(ValueError):
            link.get_url()
