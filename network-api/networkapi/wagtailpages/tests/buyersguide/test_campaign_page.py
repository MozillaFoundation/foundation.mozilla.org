from http import HTTPStatus
import json

from networkapi.wagtailpages.tests import base as test_base
from networkapi.wagtailpages import models as pagemodels
from networkapi.wagtailpages.factory import buyersguide as buyersguide_factories
from networkapi.wagtailpages.factory.donation import DonationModalFactory


class FactoriesTest(test_base.WagtailpagesTestCase):
    def test_campaign_page_factory(self):
        buyersguide_factories.BuyersGuideCampaignPageFactory()

    def test_campaign_page_donation_modal_relation_factory(self):
        buyersguide_factories.BuyersGuideCampaignPageDonationModalRelationFactory()


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

    def test_get_donation_modal_json(self):
        """
        Testing the campaign pages "get_donation_modal_json" method.

        Takes all donation modal relations, and composes a json list of dictionaries
        for use in petition.jsx.
        """
        campaign_page = buyersguide_factories.BuyersGuideCampaignPageFactory(
            parent=self.content_index
        )
        donation_modal_data = []

        for _ in range(4):
            donation_modal = DonationModalFactory()
            buyersguide_factories.BuyersGuideCampaignPageDonationModalRelationFactory(
                page=campaign_page,
                donation_modal=donation_modal,
            )
            # Using the DonationModal's "to_simple_dict" method to
            # append a dict of its values to the list.
            donation_modal_data.append(donation_modal.to_simple_dict())

        donation_modal_relations_json = json.dumps(donation_modal_data)
        list_returned_from_method = campaign_page.get_donation_modal_json()

        self.assertEqual(donation_modal_relations_json, list_returned_from_method)
        for modal in donation_modal_relations_json:
            self.assertIn(modal, list_returned_from_method)

    def test_get_donation_modal_json_with_no_modals_set(self):
        """
        Testing the campaign pages "get_donation_modal_json" method
        with no modals set. Should return empty JSON list.
        """
        campaign_page = buyersguide_factories.BuyersGuideCampaignPageFactory(
            parent=self.content_index
        )
        list_returned_from_method = campaign_page.get_donation_modal_json()

        self.assertEqual(list_returned_from_method, '[]')
