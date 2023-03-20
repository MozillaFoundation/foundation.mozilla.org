import wagtail_factories
from django.core import exceptions

from networkapi.wagtailpages.factory.research_hub import (
    detail_page as detail_page_factory,
)
from networkapi.wagtailpages.tests.research_hub import base as research_test_base


class TestResearchLibraryDetailPage(research_test_base.ResearchHubTestCase):
    def test_research_detail_page_breadcrumbs(self):
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


class TestResearchDetailLink(research_test_base.ResearchHubTestCase):
    def test_clean_with_url(self):
        link = detail_page_factory.ResearchDetailLinkFactory.build(with_url=True)

        link.clean()

        self.assertTrue(link.url)
        self.assertFalse(link.page)
        self.assertFalse(link.document)

    def test_clean_with_page(self):
        link = detail_page_factory.ResearchDetailLinkFactory.build(with_page=True)

        link.clean()

        self.assertTrue(link.page)
        self.assertFalse(link.url)
        self.assertFalse(link.document)

    def test_clean_with_doc(self):
        link = detail_page_factory.ResearchDetailLinkFactory.build(with_document=True)

        link.clean()

        self.assertTrue(link.document)
        self.assertFalse(link.url)
        self.assertFalse(link.page)

    def test_clean_with_url_and_page(self):
        link = detail_page_factory.ResearchDetailLinkFactory.build(
            with_url=True,
            with_page=True,
        )

        with self.assertRaises(exceptions.ValidationError):
            link.clean()

    def test_clean_with_url_and_doc(self):
        link = detail_page_factory.ResearchDetailLinkFactory.build(
            with_url=True,
            with_document=True,
        )

        with self.assertRaises(exceptions.ValidationError):
            link.clean()

    def test_clean_with_page_and_doc(self):
        link = detail_page_factory.ResearchDetailLinkFactory.build(
            with_url=True,
            with_page=True,
        )

        with self.assertRaises(exceptions.ValidationError):
            link.clean()

    def test_clean_with_url_and_page_and_doc(self):
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

    def test_get_url_with_url(self):
        url = "https://example.com"
        link = detail_page_factory.ResearchDetailLinkFactory.build(url=url)

        self.assertEqual(link.get_url(), url)

    def test_get_url_with_page(self):
        page = wagtail_factories.PageFactory(parent=self.homepage)
        link = detail_page_factory.ResearchDetailLinkFactory.build(page=page)

        self.assertEqual(link.get_url(), page.get_url())

    def test_get_url_with_doc(self):
        doc = wagtail_factories.DocumentFactory()
        link = detail_page_factory.ResearchDetailLinkFactory.build(document=doc)

        self.assertEqual(link.get_url(), doc.url)
