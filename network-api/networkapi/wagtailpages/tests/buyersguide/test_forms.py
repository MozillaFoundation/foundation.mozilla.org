from http import HTTPStatus

from django.test import TestCase
from wagtail.admin.edit_handlers import get_form_for_model
from wagtail.snippets.views.snippets import get_snippet_edit_handler
from wagtail.tests.utils.form_data import nested_form_data, rich_text, streamfield

from networkapi.wagtailpages import models as pagemodels
from networkapi.wagtailpages.factory import buyersguide as buyersguide_factories
from networkapi.wagtailpages.pagemodels.buyersguide.call_to_action import (
    BuyersGuideCallToAction,
)
from networkapi.wagtailpages.pagemodels.buyersguide.forms import (
    BuyersGuideArticlePageForm,
)
from networkapi.wagtailpages.tests import base as test_base


class BuyersGuideArticlePageFormTest(TestCase):
    def setUp(self):
        self.article_page_form = get_form_for_model(
            model=pagemodels.BuyersGuideArticlePage, form_class=BuyersGuideArticlePageForm
        )

    @staticmethod
    def generate_form_data(data: dict) -> dict:
        """
        Generate valid form data for the BuyersGuide article page form.

        We add the extra fields below to the dict as all these fields are set as
        required, and the form will return a validation error against them if left out.

        Since we have the "body" field set as required, we need to submit at least
        one StreamField in the form, or else the form will return a validation error.
        """
        return nested_form_data(
            {
                **data,
                "title": "Test Article Title",
                "slug": "test-article-title",
                "body": streamfield([("paragraph", rich_text("Hello world!"))]),
            }
        )

    def test_article_page_requires_search_image(self):
        """
        Test that the buyersguide article page form will
        return a validation error if no "search_image" is set.
        """
        test_form = self.article_page_form(
            data=self.generate_form_data(
                {
                    "search_description": "Test search description",
                    "search_image": None,
                },
            ),
        )

        self.assertFalse(test_form.is_valid())
        self.assertEqual(1, len(test_form.errors))
        self.assertIn("search_image", test_form.errors)
        self.assertIn("This field is required.", test_form.errors["search_image"])

    def test_article_page_requires_search_description(self):
        """
        Test that the buyersguide article page form will
        return a validation error if no "search_description" is set.
        """
        article_page = buyersguide_factories.BuyersGuideArticlePageFactory()

        test_form = self.article_page_form(
            data=self.generate_form_data(
                {
                    "search_description": None,
                    "search_image": article_page.search_image,
                },
            ),
        )

        self.assertFalse(test_form.is_valid())
        self.assertEqual(1, len(test_form.errors))
        self.assertIn("search_description", test_form.errors)
        self.assertIn("This field is required.", test_form.errors["search_description"])

    def test_article_page_requires_both_search_fields(self):
        """
        Test that the buyersguide article page form will return validation
        errors for both "search_image" and "search_description" fields
        if neither are updated.
        """
        test_form = self.article_page_form(
            data=self.generate_form_data(
                {
                    "search_description": None,
                    "search_image": None,
                },
            ),
        )

        self.assertFalse(test_form.is_valid())
        self.assertEqual(2, len(test_form.errors))
        self.assertIn("search_image", test_form.errors)
        self.assertIn("search_description", test_form.errors)
        self.assertIn("This field is required.", test_form.errors["search_image"])
        self.assertIn("This field is required.", test_form.errors["search_description"])

    def test_article_page_with_search_fields_is_valid(self):
        """
        Test that a buyersguide article page form with
        the search fields set is valid with no errors.
        """
        article_page = buyersguide_factories.BuyersGuideArticlePageFactory()

        test_form = self.article_page_form(
            data=self.generate_form_data(
                {
                    "search_description": article_page.search_description,
                    "search_image": article_page.search_image,
                },
            ),
        )

        self.assertTrue(test_form.is_valid())
        self.assertEqual(0, len(test_form.errors))
