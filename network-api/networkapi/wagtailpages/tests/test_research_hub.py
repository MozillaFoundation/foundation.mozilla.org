from django import test
from django.core import exceptions
from wagtail.tests import utils as test_utils

from networkapi.wagtailpages.factory import research_hub as research_factory
from networkapi.wagtailpages.factory import homepage as home_factory
from networkapi.wagtailpages.factory import profiles as profile_factory


class TestResearchAuthorIndexPage(test_utils.WagtailPageTests):
    def setUp(self):
        self.author_index = research_factory.ResearchAuthorsIndexPageFactory(
            parent=self.homepage,
            title="Authors"
        )

    def test_index(self):
        response = self.client.get(self.author_index.url)

        breakpoint()
        self.assertEqual(self.author_index.title, "Authors")
        self.assertEqual(response.status_code, 200)


    # def test_profile_route(self)
    #     profile = profile_factory.ProfileFactory()




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
