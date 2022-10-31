from http import HTTPStatus

from networkapi.wagtailpages.tests import base as test_base
from networkapi.wagtailpages.factory.bannered_campaign_page import BanneredCampaignPageFactory


class TestBanneredCampaignPage(test_base.WagtailpagesTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.bannered_campaign_page = BanneredCampaignPageFactory(
            parent=cls.homepage,
            title='Bannered campaign page',
            intro='I am the introduction'
        )

    def test_page_loads(self):
        url = self.bannered_campaign_page.get_url()

        response = self.client.get(path=url)

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_page_uses_intro_from_parent(self):
        self.bannered_campaign_page_child = BanneredCampaignPageFactory(
            parent=self.bannered_campaign_page,
            title='Bannered campaign page child',
            intro='I am the child introduction',
            use_intro_from_parent=True
        )
        # Ensure parent and child have same intro
        self.assertEqual(self.bannered_campaign_page_child.get_intro(), self.bannered_campaign_page.intro)
