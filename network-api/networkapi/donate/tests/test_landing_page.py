from http import HTTPStatus

from wagtail.models import Page as WagtailPage

from networkapi.donate.factory import landing_page as landing_page_factories
from networkapi.donate import models as pagemodels
from networkapi.wagtailpages.tests import base as test_base


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
        Testing that the DonateLandingPage model can only be created at the root level.
        """
        self.assertAllowedParentPageTypes(
            child_model=pagemodels.DonateLandingPage,
            parent_models={WagtailPage},
        )

    def test_subpage_types(self):
        """
        Testing the DonateLandingPage's allowed subpage types.
        """
        self.assertAllowedSubpageTypes(
            parent_model=pagemodels.DonateLandingPage,
            child_models={pagemodels.DonateHelpPage},
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
