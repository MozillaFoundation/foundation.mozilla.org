from http import HTTPStatus

from wagtail.models import Page as WagtailPage

from networkapi.donate import factory as donate_factories
from networkapi.donate import models as pagemodels
from networkapi.wagtailpages.tests import base as test_base


class FactoriesTest(test_base.WagtailpagesTestCase):
    def test_page_factory(self):
        """
        Testing the factory can successfully create a DonateHelpPage.
        """
        donate_factories.DonateHelpPageFactory()


class DonateHelpPageTest(test_base.WagtailpagesTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.donate_landing_page = donate_factories.DonateHelpPageFactory(
            parent=cls.homepage,
        )
        cls.donate_help_page = donate_factories.DonateHelpPageFactory(
            parent=cls.donate_landing_page,
        )

    def test_parent_page_types(self):
        """
        Testing that the DonateHelpPage model can only be created as a child of a landing page.
        """
        self.assertAllowedParentPageTypes(
            child_model=pagemodels.DonateHelpPage,
            parent_models={pagemodels.DonateLandingPage},
        )

    def test_subpage_types(self):
        """
        Testing the DonateHelpPage's allowed subpage types.
        """
        self.assertAllowedSubpageTypes(
            parent_model=pagemodels.DonateHelpPage,
            child_models={},
        )

    def test_page_success(self):
        """
        Testing that visiting a DonateHelpPage's URL returns a successful HTTP status.
        """
        url = self.donate_help_page.get_url()

        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_template(self):
        """
        Testing that visiting a DonateHelpPage's URL renders the correct templates.
        """
        url = self.donate_help_page.get_url()

        response = self.client.get(url)

        self.assertTemplateUsed(
            response=response,
            template_name="donate/pages/help_page.html",
        )
