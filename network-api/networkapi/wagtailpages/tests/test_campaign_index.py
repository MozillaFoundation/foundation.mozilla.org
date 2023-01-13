import http

from networkapi.wagtailpages.factory import campaign_page as campaign_factories
from networkapi.wagtailpages.tests import test_index


class CampaignIndexPageTests(test_index.IndexPageTestCase):
    index_page_factory = campaign_factories.CampaignIndexPageFactory

    def test_factory(self):
        campaign_factories.CampaignIndexPageFactory()

        self.assertTrue(True)

    def test_page_load(self):
        response = self.client.get(path=self.index_page.get_url())

        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertContains(response, self.index_page.title)
