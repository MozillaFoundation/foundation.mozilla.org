from django import test

from networkapi.wagtailpages.wagtail_hooks import (
    RichTextExternalLinkNewTabHandler as external_link_handler,
)


class RichTextExternalLinkTest(test.TestCase):
    def test_whitelisted_external_links_all(self):
        attrs = {"href": "https://www.google.com/"}
        external_link_handler.whitelisted_external_links = ["*"]
        expected_output = '<a href="https://www.google.com/" target="_blank">'
        self.assertEqual(external_link_handler.expand_db_attributes(attrs), expected_output)

    def test_whitelisted_external_links_none(self):
        attrs = {"href": "https://www.google.com/"}
        external_link_handler.whitelisted_external_links = []
        expected_output = '<a href="https://www.google.com/" target="_blank" rel="nofollow">'
        self.assertEqual(external_link_handler.expand_db_attributes(attrs), expected_output)

    def test_whitelisted_external_links_negative(self):
        attrs = {"href": "https://www.google.com/"}
        external_link_handler.whitelisted_external_links = ["bing.", "yahoo."]
        expected_output = '<a href="https://www.google.com/" target="_blank" rel="nofollow">'
        self.assertEqual(external_link_handler.expand_db_attributes(attrs), expected_output)

    def test_whitelisted_external_links_positive(self):
        attrs = {"href": "https://www.google.com/"}
        external_link_handler.whitelisted_external_links = ["google.", "yahoo."]
        expected_output = '<a href="https://www.google.com/" target="_blank">'
        self.assertEqual(external_link_handler.expand_db_attributes(attrs), expected_output)
