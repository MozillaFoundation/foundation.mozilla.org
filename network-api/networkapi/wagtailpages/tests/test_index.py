from http import HTTPStatus

from wagtail.core import models as wagtail_models

from networkapi.wagtailpages.factory import index_page as index_factory
from networkapi.wagtailpages.factory import publication as publication_factory
from networkapi.wagtailpages.tests import base as test_base


class IndexPageTests(test_base.WagtailpagesTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.index_page = index_factory.IndexPageFactory(parent=cls.homepage)

    def test_GET_child_in_entries(self):
        """
        Currently, this is returning the generic page type, which requires the use of
        `.specific` in the templates. That is probably causing the n+1 which the cache is
        used to cricumvent. We should probably not be doing that in the template and return
        the proper pages in the context.

        TODO: Refactor implementation to return specific page types of child pages.
        """
        article_page = publication_factory.ArticlePageFactory(parent=self.index_page)
        generic_child_page = wagtail_models.Page.objects.get(id=article_page.id)

        response = self.client.get(path=self.index_page.get_url())

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(generic_child_page, response.context["entries"])

    def test_GET_entries_have_same_locale_as_index_page(self):
        article_page = publication_factory.ArticlePageFactory(parent=self.index_page)
        self.synchronize_tree()
        fr_index_page = self.index_page.get_translation(self.fr_locale)

        response = self.client.get(path=fr_index_page.get_url())

        self.assertEqual(response.status_code, HTTPStatus.OK)
        fr_entry_page = response.context["entries"][0]
        self.assertNotEqual(fr_entry_page.id, article_page.id)
        self.assertEqual(fr_entry_page.locale, self.fr_locale)
