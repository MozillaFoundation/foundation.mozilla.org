from django.test import TestCase
from wagtail.admin.panels import get_edit_handler

from networkapi.wagtailpages.factory import buyersguide as buyersguide_factories
from networkapi.wagtailpages.pagemodels.buyersguide.call_to_action import (
    BuyersGuideCallToAction,
)


class BuyersGuideCallToActionTest(TestCase):
    def setUp(self):
        edit_handler = get_edit_handler(BuyersGuideCallToAction)
        self.form_class = edit_handler.get_form_class()

    def test_return_target_url_with_external_link(self):
        test_url = "http://test.com"
        cta = BuyersGuideCallToAction.objects.create(
            title="Test CTA",
            link_label="Test Link",
            link_target_url=test_url,
        )
        cta.save()

        target_url = cta.get_target_url()

        self.assertEqual(target_url, test_url)

    def test_return_target_url_with_page_link(self):
        test_page = buyersguide_factories.BuyersGuidePageFactory()
        cta = BuyersGuideCallToAction.objects.create(
            title="Test CTA",
            link_label="Test Link",
            link_target_page=test_page,
        )
        cta.save()

        target_url = cta.get_target_url()

        self.assertEqual(target_url, test_page.url)

    def test_cta_with_no_link_or_label_is_valid(self):
        form = self.form_class(
            data=(
                {
                    "title": "Test CTA",
                }
            )
        )

        self.assertTrue(form.is_valid())
        self.assertEqual(0, len(form.errors))

    def test_cta_cannot_have_label_and_both_external_and_page_link(self):
        test_page = buyersguide_factories.BuyersGuidePageFactory()
        form = self.form_class(
            data=(
                {
                    "title": "Test CTA",
                    "link_label": "Test Link",
                    "link_target_url": "http://test.com",
                    "link_target_page": test_page,
                }
            )
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(2, len(form.errors))
        self.assertIn("link_target_url", form.errors)
        self.assertIn("link_target_page", form.errors)

    def test_page_link_and_label_is_valid(self):
        test_page = buyersguide_factories.BuyersGuidePageFactory()
        form = self.form_class(
            data=(
                {
                    "title": "Test CTA",
                    "link_label": "Test Link",
                    "link_target_page": test_page,
                }
            )
        )

        self.assertTrue(form.is_valid())
        self.assertEqual(0, len(form.errors))

    def test_page_link_without_label_is_invalid(self):
        test_page = buyersguide_factories.BuyersGuidePageFactory()
        form = self.form_class(
            data=({"title": "Test CTA", "link_target_page": test_page}),
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(1, len(form.errors))
        self.assertIn("link_label", form.errors)

    def test_external_link_and_label_is_valid(self):
        form = self.form_class(
            data=(
                {
                    "title": "Test CTA",
                    "link_label": "Test Link",
                    "link_target_url": "http://test.com",
                }
            )
        )

        self.assertTrue(form.is_valid())
        self.assertEqual(0, len(form.errors))

    def test_external_link_without_label_is_invalid(self):
        form = self.form_class(
            data=({"title": "Test CTA", "link_target_url": "http://test.com"}),
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(1, len(form.errors))
        self.assertIn("link_label", form.errors)

    def test_label_must_also_have_external_or_page_link(self):
        form = self.form_class(
            data=({"title": "Test CTA", "link_label": "Test Link"}),
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(2, len(form.errors))
        self.assertIn("link_target_url", form.errors)
        self.assertIn("link_target_page", form.errors)

    def test_external_and_page_link_without_label_is_invalid(self):
        test_page = buyersguide_factories.BuyersGuidePageFactory()
        form = self.form_class(
            data=(
                {
                    "title": "Test CTA",
                    "link_target_url": "http://test.com",
                    "link_target_page": test_page,
                }
            )
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(1, len(form.errors))
        self.assertIn("link_label", form.errors)

    def test_link_target_url_valid_formats(self):
        valid_urls = [
            "http://example.com",
            "https://example.com",
            "http://www.example.com",
            "https://www.example.com",
            "http://example.com/test_underscore",
            "http://example.com/test_(parenthesis)",
            "https://example.com/path/to/page?param1=value1&param2=value2[1]&param3=value3[2]",
            "https://example.com/path/?list_of_params=1,2,3"
            "http://www.example.com/test/?p=364",
            "https://www.example.com/test/?param1=value1&param2=42&other_param",
            "http://example.com/page#cite-1",
            "http://example.com/path/to/page/#cite-1",
            "http://example.com/path/to/page/#cite-1?with_params=true",
            "http://example.com/path/to/page/#cite-1/?with_params=true",
            "http://example.com/path/to/page/#cite-1/?param_1=value1&param_2=value2",
            "http://example.bar/?q=Test%20URL-encoded%20stuff",
            "http://example.com?param_1=value_1",
            "http://example.com/?param_1=value_1&param2=value2",
            "?param_1=value1",
            "?param_1=value1&param_2=value2",
            "?param_1=value1&param_2=1234",
        ]

        for url in valid_urls:
            with self.subTest(name=url):
            # Do test and assertions
                data = {
                    "title": "Test CTA",
                    "link_label": "Test Link",
                    "link_target_url": url,
                }
                form = self.form_class(data=data)

                self.assertTrue(form.is_valid())

    def test_link_target_url_invalid_formats(self):
        invalid_urls = [
            "example.com",
            "not_a_valid_string",
            "not a valid string",
            "invalid_param=test",
            "http://example.com?q=Spaces should be encoded",
            "//test",
            "http:// example.com",
        ]

        for url in invalid_urls:
            with self.subTest(name=url):
                data = {
                    "title": "Test CTA",
                    "link_label": "Test Link",
                    "link_target_url": url,
                }
                form = self.form_class(data=data)

                self.assertFalse(form.is_valid())
                self.assertEqual(1, len(form.errors))
                self.assertIn("link_target_url", form.errors)
