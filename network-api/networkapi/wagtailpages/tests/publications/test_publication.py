import http

from networkapi.wagtailpages.factory import publication as publication_factory
from networkapi.wagtailpages.tests import base as test_base


class PublicationPageTests(test_base.WagtailpagesTestCase):
    def test_factory(self):
        publication_factory.PublicationPageFactory()

        self.assertTrue(True)

    def test_page_loads(self):
        publication_page = publication_factory.PublicationPageFactory(parent=self.homepage)

        response = self.client.get(path=publication_page.get_url())

        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertContains(response, publication_page.title)

    def test_page_w_child_loads(self):
        publication_page = publication_factory.PublicationPageFactory(parent=self.homepage)
        publication_factory.PublicationPageFactory(parent=publication_page)

        response = self.client.get(path=publication_page.get_url())

        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertContains(response, publication_page.title)
