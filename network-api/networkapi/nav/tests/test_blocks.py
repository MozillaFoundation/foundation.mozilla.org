from django.test import TestCase
from wagtail.blocks import StreamBlockValidationError
from wagtail.models import Locale, Page

from networkapi.nav.blocks import NavLinkBlock
from networkapi.nav.factories import NavLinkBlockFactory


class TestLinkBlock(TestCase):
    def test_default(self):
        """Assert that default NavLinkBlock factory works and is an external URL."""
        block = NavLinkBlockFactory()

        # Assert that the page link is custom URL and that it is correct
        url = block["external_url"]
        self.assertEqual(block.url, url)

    def test_page_link(self):
        """Create a NavLinkBlock with a page link."""
        block = NavLinkBlockFactory(page_link=True)

        page = block["page"]
        self.assertIsNotNone(page)
        self.assertTrue(isinstance(page, Page))
        default_locale = Locale.get_default()
        self.assertEqual(page.locale, default_locale)

        self.assertFalse(block.open_in_new_window)

        # Assert that other fields are empty
        self.assertEqual(block["external_url"], "")
        self.assertEqual(block["relative_url"], "")

    def test_external_url_link(self):
        """Create a NavLinkBlock with a custom/external URL."""
        block = NavLinkBlockFactory(external_url_link=True)

        # Assert that the URL is a URL
        url = block["external_url"]
        self.assertIsNotNone(url)

        self.assertTrue(block.open_in_new_window)

        # Assert that other fields are empty
        self.assertIsNone(block["page"])
        self.assertEqual(block["relative_url"], "")

    def test_relative_url_link(self):
        """Create a NavLinkBlock with a relative URL."""
        block = NavLinkBlockFactory(relative_url_link=True)

        # Assert that the URL is a URL
        url = block["relative_url"]
        self.assertIsNotNone(url)

        self.assertFalse(block.open_in_new_window)

        # Assert that other fields are empty
        self.assertIsNone(block["page"])
        self.assertEqual(block["external_url"], "")

    def test_needs_to_provide_at_least_one_link(self):
        with self.assertRaises(StreamBlockValidationError):
            block = NavLinkBlockFactory()
            NavLinkBlock().clean(block)
