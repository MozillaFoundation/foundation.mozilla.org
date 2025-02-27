from django.test import TestCase
from wagtail.admin.panels import get_form_for_model
from wagtail.test.utils.form_data import nested_form_data, rich_text, streamfield

from legacy_cms.wagtailpages import models as pagemodels
from legacy_cms.wagtailpages.factory.image_factory import ImageFactory
from legacy_cms.wagtailpages.pagemodels.buyersguide.forms import (
    BuyersGuideArticlePageForm,
)


class BuyersGuideArticlePageFormTest(TestCase):
    def setUp(self):
        self.article_page_form = get_form_for_model(
            model=pagemodels.BuyersGuideArticlePage,
            form_class=BuyersGuideArticlePageForm,
            fields=["search_description", "search_image"],
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

        test_form = self.article_page_form(
            data=self.generate_form_data(
                {
                    "search_description": None,
                    "search_image": ImageFactory().id,
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

        test_form = self.article_page_form(
            data=self.generate_form_data(
                {
                    "search_description": "Test search description",
                    "search_image": ImageFactory().id,
                },
            ),
        )

        self.assertTrue(test_form.is_valid())
        self.assertEqual(0, len(test_form.errors))
