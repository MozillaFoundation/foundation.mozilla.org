from http import HTTPStatus

from wagtail.models import Page as WagtailPage

from networkapi.donate import factory as donate_factories
from networkapi.donate import models as pagemodels
from networkapi.wagtailpages.tests import base as test_base


class FactoriesTest(test_base.WagtailpagesTestCase):
    def test_page_factory(self):
        donate_factories.DonateLandingPageFactory()


class DonateLandingPageTest(test_base.WagtailpagesTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.donate_landing_page = donate_factories.DonateLandingPageFactory(
            parent=cls.homepage,
        )

    def test_parents(self):
        self.assertAllowedParentPageTypes(
            child_model=pagemodels.DonateLandingPage,
            parent_models={WagtailPage},
        )

    def test_children(self):
        self.assertAllowedSubpageTypes(
            parent_model=pagemodels.DonateLandingPage,
            child_models={},
        )

    def test_page_success(self):
        url = self.donate_landing_page.get_url()

        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_template(self):
        url = self.donate_landing_page.get_url()

        response = self.client.get(url)

        self.assertTemplateUsed(
            response=response,
            template_name="pages/landing_page.html",
        )
