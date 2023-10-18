from http import HTTPStatus

from networkapi.donate import models as pagemodels
from networkapi.donate.factory import help_page as help_page_factories
from networkapi.wagtailpages.tests import base as test_base


class FactoriesTest(test_base.WagtailpagesTestCase):
    def test_page_factory(self):
        """
        Testing the factory can successfully create a DonateHelpPage.
        """
        help_page_factories.DonateHelpPageFactory()


class DonateHelpPageTest(test_base.WagtailpagesTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.donate_landing_page = help_page_factories.DonateHelpPageFactory(
            parent=cls.homepage,
        )
        cls.donate_help_page = help_page_factories.DonateHelpPageFactory(
            parent=cls.donate_landing_page,
            notice__0="notice",
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

    def test_help_page_notice_field(self):
        """
        Asserts that a 'notice' block was created in the 'notice' field by the factory.
        """
        self.assertEqual(self.donate_help_page.notice[0].block_type, "notice")
