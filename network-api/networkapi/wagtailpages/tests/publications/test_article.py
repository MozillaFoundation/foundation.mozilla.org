import http

from networkapi.wagtailpages.factory import publication as publication_factory
from networkapi.wagtailpages.tests import base as test_base


class ArticePageTests(test_base.WagtailpagesTestCase):
    def test_factory(self):
        publication_factory.ArticlePageFactory()

        self.assertTrue(True)

    def test_page_loads(self):
        artice_page = publication_factory.ArticlePageFactory(parent=self.homepage)

        response = self.client.get(path=artice_page.get_url())

        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertContains(response, artice_page.title)
