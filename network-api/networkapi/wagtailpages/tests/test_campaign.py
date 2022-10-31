from http import HTTPStatus

from networkapi.wagtailpages.tests import base as test_base
from networkapi.wagtailpages.factory.bannered_campaign_page import BanneredCampaignPageFactory


class TestBanneredCampaignPage(test_base.WagtailpagesTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.bannered_campaign_page = BanneredCampaignPageFactory.create(
            parent=cls.homepage,
            title='Bannered campaign page',
            intro='I am the introduction'
        )

    def test_page_loads(self):
        BanneredCampaignPageFactory(parent=self.bannered_campaign_page)
        url = self.bannered_campaign_page.get_url()

        response = self.client.get(path=url)

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_page_uses_intro_from_parent(self):
        bannered_campaign_page_child = BanneredCampaignPageFactory(
            parent=self.bannered_campaign_page,
            use_intro_from_parent=True
        )

        self.assertEqual(bannered_campaign_page_child.intro, self.bannered_campaign_page.intro)
