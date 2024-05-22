from http import HTTPStatus

from networkapi.donate import models as pagemodels
from networkapi.donate.factory import help_page as help_page_factories
from networkapi.donate.factory.snippets import (
    help_page_notice as help_page_notice_factories,
)
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

    def test_thank_you_url(self):
        """
        Testing that the "thank_you_url" is correctly added to the page context.
        """
        page_url = self.donate_help_page.get_full_url()
        response = self.client.get(page_url)

        expected_thank_you_url = page_url + "?thank_you=true"

        self.assertEqual(response.context["thank_you_url"], expected_thank_you_url)

    def test_thank_you_url_with_existing_query_params(self):
        """
        Testing that the "thank_you_url" is correctly added to the page context when there
        are existing query parameters.
        """
        page_url = self.donate_help_page.get_full_url() + "?existing_param=value"
        response = self.client.get(page_url)

        expected_thank_you_url = page_url + "&thank_you=true"

        self.assertEqual(response.context["thank_you_url"], expected_thank_you_url)

    def test_page_displays_help_page_notice(self):
        """
        Test that the DonateHelpPage correctly displays the HelpPageNotice.
        """
        notice_text_content = "<p>Test Notice Content</p>"
        help_page_notice = help_page_notice_factories.HelpPageNoticeFactory(text=notice_text_content)
        self.donate_help_page.notice = help_page_notice
        self.donate_help_page.save()

        url = self.donate_help_page.get_url()
        response = self.client.get(url)

        self.assertContains(response, notice_text_content)
