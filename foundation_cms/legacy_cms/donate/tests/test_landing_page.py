from http import HTTPStatus

from foundation_cms.legacy_cms.donate.factory import (
    landing_page as landing_page_factories,
)
from foundation_cms.legacy_cms.donate.models import DonateHelpPage, DonateLandingPage
from foundation_cms.legacy_cms.wagtailpages.models import Homepage, OpportunityPage
from foundation_cms.legacy_cms.wagtailpages.tests import base as test_base


class FactoriesTest(test_base.WagtailpagesTestCase):
    def test_page_factory(self):
        """
        Testing the factory can successfully create a DonateLandingPage.
        """
        landing_page_factories.DonateLandingPageFactory()


class DonateLandingPageTest(test_base.WagtailpagesTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.donate_landing_page = landing_page_factories.DonateLandingPageFactory(
            parent=cls.homepage,
        )

    def test_parent_page_types(self):
        """
        Testing that the DonateLandingPage model can only be created under the Homepage level.
        """
        self.assertAllowedParentPageTypes(
            child_model=DonateLandingPage,
            parent_models={Homepage},
        )

    def test_subpage_types(self):
        """
        Testing the DonateLandingPage's allowed subpage types.
        """
        self.assertAllowedSubpageTypes(
            parent_model=DonateLandingPage,
            child_models={DonateHelpPage, OpportunityPage},
        )

    def test_page_success(self):
        """
        Testing that visiting a DonateLandingPage's URL returns a successful HTTP status.
        """
        url = self.donate_landing_page.get_url()

        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_template(self):
        """
        Testing that visiting a DonateLandingPage's URL renders the correct templates.
        """
        url = self.donate_landing_page.get_url()

        response = self.client.get(url)

        self.assertTemplateUsed(
            response=response,
            template_name="donate/pages/landing_page.html",
        )
