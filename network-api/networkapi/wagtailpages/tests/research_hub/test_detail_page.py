from django import test
from django.core import exceptions

from networkapi.wagtailpages.factory import research_hub as research_factory
from networkapi.wagtailpages.tests.research_hub import base as research_test_base


class TestResearchDetailLink(test.TestCase):
    def test_clean_with_url(self):
        link = research_factory.ResearchDetailLinkFactory.build(with_url=True)

        link.clean()

        self.assertTrue(link.url)
        self.assertFalse(link.document)

    def test_clean_with_doc(self):
        link = research_factory.ResearchDetailLinkFactory.build(with_document=True)

        link.clean()

        self.assertTrue(link.document)
        self.assertFalse(link.url)

    def test_clean_with_url_and_doc(self):
        link = research_factory.ResearchDetailLinkFactory.build(
            with_url=True,
            with_document=True,
        )

        with self.assertRaises(exceptions.ValidationError):
            link.clean()

    def test_clean_with_neither_url_nor_doc(self):
        link = research_factory.ResearchDetailLinkFactory.build()

        with self.assertRaises(exceptions.ValidationError):
            link.clean()


class TestResearchLibraryDetailPage(research_test_base.ResearchHubTestCase):

    def test_research_detail_page_breadcrumbs(self):
        detail_page = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
        )
        response = self.client.get(detail_page.url)
        breadcrumbs = response.context['breadcrumbs']
        expected_breadcrumbs = [{'title': 'Research', 'url': '/en/research/'},
                                {'title': 'Library', 'url': '/en/research/library/'}]

        self.assertEqual(len(breadcrumbs), 2)
        self.assertEqual(breadcrumbs, expected_breadcrumbs)
