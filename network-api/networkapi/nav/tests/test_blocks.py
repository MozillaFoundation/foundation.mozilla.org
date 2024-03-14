from django.test import TestCase
from wagtail.blocks import StreamBlockValidationError
from wagtail.models import Locale, Page

from networkapi.nav import blocks as nav_blocks
from networkapi.nav import factories as nav_factories


class TestNavItemBlock(TestCase):
    def test_default(self):
        """Assert that default nav_blocks.NavItem factory works and is an external URL."""
        block = nav_factories.NavItemFactory()

        # Assert that the page link is custom URL and that it is correct
        url = block["external_url"]
        self.assertEqual(block.url, url)

    def test_page_link(self):
        """Create a nav_blocks.NavItem with a page link."""
        block = nav_factories.NavItemFactory(page_link=True)

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
        """Create a nav_blocks.NavItem with a custom/external URL."""
        block = nav_factories.NavItemFactory(external_url_link=True)

        # Assert that the URL is a URL
        url = block["external_url"]
        self.assertIsNotNone(url)

        self.assertTrue(block.open_in_new_window)

        # Assert that other fields are empty
        self.assertIsNone(block["page"])
        self.assertEqual(block["relative_url"], "")

    def test_relative_url_link(self):
        """Create a nav_blocks.NavItem with a relative URL."""
        block = nav_factories.NavItemFactory(relative_url_link=True)

        # Assert that the URL is a URL
        url = block["relative_url"]
        self.assertIsNotNone(url)

        self.assertFalse(block.open_in_new_window)

        # Assert that other fields are empty
        self.assertIsNone(block["page"])
        self.assertEqual(block["external_url"], "")

    def test_needs_to_provide_at_least_one_link(self):
        with self.assertRaises(StreamBlockValidationError):
            block = nav_factories.NavItemFactory()
            nav_blocks.NavItem().clean(block)


class TestNavButton(TestCase):
    def test_default(self):
        """Assert that default nav_blocks.NavButton factory works and is an external URL."""
        block = nav_factories.NavButtonFactory()

        # Assert that the page link is custom URL and that it is correct
        url = block["external_url"]
        self.assertEqual(block.url, url)

    def test_page_link(self):
        """Create a nav_blocks.NavButton with a page link."""
        block = nav_factories.NavButtonFactory(page_link=True)

        page = block["page"]
        self.assertIsNotNone(page)
        self.assertTrue(isinstance(page, Page))
        default_locale = Locale.get_default()
        self.assertEqual(page.locale, default_locale)

        # Assert that other fields are empty
        self.assertEqual(block["external_url"], "")
        self.assertEqual(block["relative_url"], "")

    def test_external_url_link(self):
        """Create a nav_blocks.NavButton with a custom/external URL."""
        block = nav_factories.NavButtonFactory(external_url_link=True)

        # Assert that the URL is a URL
        url = block["external_url"]
        self.assertIsNotNone(url)

        # Assert that other fields are empty
        self.assertIsNone(block["page"])
        self.assertEqual(block["relative_url"], "")

    def test_relative_url_link(self):
        """Create a nav_blocks.NavButton with a relative URL."""
        block = nav_factories.NavButtonFactory(relative_url_link=True)

        # Assert that the URL is a URL
        url = block["relative_url"]
        self.assertIsNotNone(url)

        # Assert that other fields are empty
        self.assertIsNone(block["page"])
        self.assertEqual(block["external_url"], "")

    def test_needs_to_provide_at_least_one_link(self):
        with self.assertRaises(StreamBlockValidationError):
            block = nav_factories.NavItemFactory()
            nav_blocks.NavItem().clean(block)
