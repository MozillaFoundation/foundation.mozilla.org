from django.test import TestCase
from wagtail.admin.panels import get_edit_handler
from wagtail.test.utils.form_data import rich_text

from foundation_cms.legacy_apps.wagtailpages.donation_modal import DonationModal


class DonationModalTest(TestCase):
    def setUp(self):
        edit_handler = get_edit_handler(DonationModal)
        self.form_class = edit_handler.get_form_class()

    def test_link_target_url_valid_formats(self):
        valid_urls = [
            "http://example.com",
            "https://example.com",
            "http://www.example.com",
            "https://www.example.com",
            "http://example.com/test_underscore",
            "http://example.com/test_(parenthesis)",
            "https://example.com/path/to/page?param1=value1&param2=value2[1]&param3=value3[2]",
            "https://example.com/path/?list_of_params=1,2,3",
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
                data = {
                    "name": "Test Name",
                    "header": "Test Header",
                    "body": rich_text("<p>Test Body</p>"),
                    "donate_text": "Test Donate Button Text",
                    "donate_url": url,
                    "dismiss_text": "Test Dismiss Text",
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
                    "name": "Test Name",
                    "header": "Test Header",
                    "body": rich_text("<p>Test Body</p>"),
                    "donate_text": "Test Donate Button Text",
                    "donate_url": url,
                    "dismiss_text": "Test Dismiss Text",
                }
                form = self.form_class(data=data)

                self.assertFalse(form.is_valid())
                self.assertEqual(1, len(form.errors))
                self.assertIn("donate_url", form.errors)
