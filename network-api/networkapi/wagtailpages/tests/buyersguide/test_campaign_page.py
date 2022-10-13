from http import HTTPStatus

from networkapi.wagtailpages.tests import base as test_base
from networkapi.wagtailpages import models as pagemodels
from networkapi.wagtailpages.factory import buyersguide as buyersguide_factories


class BuyersGuideCampaignPageTest(test_base.WagtailpagesTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.buyersguide_homepage = buyersguide_factories.BuyersGuidePageFactory(
            parent=cls.homepage,
        )
        cls.content_index = buyersguide_factories.BuyersGuideEditorialContentIndexPageFactory(
            parent=cls.buyersguide_homepage,
        )

    def test_parents(self):
        self.assertAllowedParentPageTypes(
            child_model=pagemodels.BuyersGuideCampaignPage,
            parent_models={pagemodels.BuyersGuideEditorialContentIndexPage},
        )

    def test_children(self):
        self.assertAllowedSubpageTypes(
            parent_model=pagemodels.BuyersGuideCampaignPage,
            child_models={},
        )

    def test_page_success(self):
        campaign_page = buyersguide_factories.BuyersGuideCampaignPageFactory(
            parent=self.content_index,
        )

        response = self.client.get(campaign_page.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_template(self):
        campaign_page = buyersguide_factories.BuyersGuideCampaignPageFactory(
            parent=self.content_index,
        )

        response = self.client.get(campaign_page.url)

        self.assertTemplateUsed(
            response=response,
            template_name='pages/buyersguide/campaign_page.html',
        )
        self.assertTemplateUsed(
            response=response,
            template_name='pages/buyersguide/base.html',
        )
        self.assertTemplateUsed(
            response=response,
            template_name='pages/base.html',
        )

    def test_content_template(self):
        campaign_page = buyersguide_factories.BuyersGuideCampaignPageFactory(
            parent=self.content_index,
        )

        response = self.client.get(campaign_page.url)

        self.assertTemplateUsed(
            response=response,
            template_name='wagtailpages/blocks/rich_text_block.html',
        )
