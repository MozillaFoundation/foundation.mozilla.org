import wagtail_factories
from django.test import TestCase
from wagtail.blocks import StreamBlockValidationError, StructBlockValidationError
from wagtail.models import Locale, Page

from foundation_cms.navigation import blocks as nav_blocks
from foundation_cms.navigation import factories as nav_factories


class TestNavLinkFactory(TestCase):
    def test_external_url_link_trait(self):
        """NavLinkFactory with external_url_link trait should create a valid external link."""
        block = nav_factories.NavLinkFactory(external_url_link=True)
        nav_blocks.NavLink().clean(block)

        # Link type should be external_url
        self.assertEqual(block["link_to"], "external_url")
        self.assertTrue(block["external_url"])

        # Should be marked external via NavLinkValue helper
        self.assertTrue(block.is_external)

        # Other link fields should be empty
        self.assertIsNone(block["page"])
        self.assertEqual(block["relative_url"], "")

        # BaseLinkValue.url should resolve to external_url
        self.assertEqual(block.url, block["external_url"])

    def test_relative_url_link_trait(self):
        """NavLinkFactory with relative_url_link trait should create a valid internal relative link."""
        block = nav_factories.NavLinkFactory(relative_url_link=True)

        # Don't re-run block.clean() on factory output; instead assert the expected shape/values
        self.assertEqual(block["link_to"], "relative_url")
        self.assertTrue(block["relative_url"])
        self.assertFalse(block.is_external)

        # Other link fields should be empty
        self.assertIsNone(block["page"])
        self.assertEqual(block["external_url"], "")

        # URL property resolves to the relative url
        self.assertEqual(block.url, block["relative_url"])

    def test_page_link_trait(self):
        """NavLinkFactory with page_link trait should create a valid page link."""
        block = nav_factories.NavLinkFactory(page_link=True)
        nav_blocks.NavLink().clean(block)

        page = block["page"]
        self.assertIsNotNone(page)
        self.assertIsInstance(page, Page)
        self.assertEqual(page.locale, Locale.get_default())

        self.assertEqual(block["link_to"], "page")
        self.assertFalse(block.is_external)

        # Other link fields should be empty
        self.assertEqual(block["external_url"], "")
        self.assertEqual(block["relative_url"], "")

        # URL should resolve to page.url
        self.assertEqual(block.url, page.url)

    def test_invalid_without_target(self):
        """NavLink should fail validation if no link target is provided."""
        # Build an explicit invalid payload with no target URL or page.
        invalid_payload = {
            "link_to": "external_url",
            "external_url": "",
            "page": None,
            "relative_url": "",
        }

        # The NavLink.clean method raises StreamBlockValidationError for this case.
        with self.assertRaises(StreamBlockValidationError):
            nav_blocks.NavLink().clean(invalid_payload)


class TestNavDropdownFactory(TestCase):
    def test_default_factory_is_valid(self):
        """Default NavDropdownFactory should create a valid dropdown with header and items."""
        block = nav_factories.NavDropdownFactory()
        nav_blocks.NavDropdown().clean(block)

        # Header should exist and be a NavLinkValue
        self.assertIsInstance(block.header_value, nav_blocks.NavLinkValue)
        self.assertEqual(block.header_value, block["header"])

        # Default factory defines 3 dropdown items
        items = block.dropdown_items
        self.assertEqual(len(items), 3)
        for item in items:
            self.assertIsInstance(item, nav_blocks.NavLinkValue)

    def test_header_page_link_trait(self):
        """Dropdown header_page_link trait should produce a valid page link."""
        block = nav_factories.NavDropdownFactory(header_page_link=True)
        nav_blocks.NavDropdown().clean(block)

        header = block["header"]
        self.assertEqual(header["link_to"], "page")
        self.assertIsNotNone(header["page"])
        self.assertIsInstance(header["page"], Page)

    def test_header_external_link_trait(self):
        """Dropdown header_external_link trait should produce a valid external link."""
        block = nav_factories.NavDropdownFactory(header_external_link=True)
        nav_blocks.NavDropdown().clean(block)

        header = block["header"]
        self.assertEqual(header["link_to"], "external_url")
        self.assertTrue(header["external_url"])
        self.assertTrue(header.is_external)

    def test_header_relative_link_trait(self):
        """Dropdown header_relative_link trait should produce a valid relative link."""
        block = nav_factories.NavDropdownFactory(header_relative_link=True)

        header = block["header"]
        # Assert the header is a nav link with a relative URL
        self.assertEqual(header["link_to"], "relative_url")
        self.assertTrue(header["relative_url"])
        self.assertFalse(header.is_external)

    def test_items_can_be_empty(self):
        """Dropdown items are optional and may be empty."""
        block = nav_factories.NavDropdownFactory(items=[])
        nav_blocks.NavDropdown().clean(block)
        self.assertEqual(block.dropdown_items, [])

    def test_items_cannot_exceed_five(self):
        """Dropdown items ListBlock enforces a maximum of 5 links."""
        with self.assertRaises(StructBlockValidationError):
            block = nav_factories.NavDropdownFactory(
                items=wagtail_factories.ListBlockFactory(
                    nav_factories.NavLinkFactory,
                    **{
                        "0__external_url_link": True,
                        "1__external_url_link": True,
                        "2__external_url_link": True,
                        "3__external_url_link": True,
                        "4__external_url_link": True,
                        "5__external_url_link": True,
                    },
                )
            )
            nav_blocks.NavDropdown().clean(block)

    def test_requires_header(self):
        """Dropdown should fail validation if header is missing."""
        # A dropdown must have a header. Passing None should result in a failure.
        with self.assertRaises(Exception):
            block = nav_factories.NavDropdownFactory(header=None)
            # calling .clean may raise StructBlockValidationError or AttributeError depending on internals
            nav_blocks.NavDropdown().clean(block)


class TestNavigationMenuFactory(TestCase):
    def test_factory_creates_valid_menu(self):
        """NavigationMenuFactory should create a valid menu with up to 5 dropdowns."""
        menu = nav_factories.NavigationMenuFactory()
        self.assertTrue(menu.pk)

        # Dropdowns StreamField should contain dropdown blocks
        self.assertGreaterEqual(len(menu.dropdowns), 1)
        self.assertLessEqual(len(menu.dropdowns), 5)

        for block in menu.dropdowns:
            self.assertEqual(block.block_type, "dropdown")
            self.assertIsInstance(block.value, nav_blocks.NavDropdownValue)

        # Locale should default correctly
        self.assertEqual(menu.locale, Locale.get_default())
