from django.test import TestCase
from django.utils.translation import gettext_lazy as _
from wagtail.blocks import StreamBlockValidationError
from wagtail.documents.models import Document
from wagtail.models import Locale, Page
from wagtail_link_block.blocks import LinkBlock as WagtailLinkBlock

from networkapi.wagtailpages.factory import customblocks as customblock_factories


class TesWagtailLinkBlock(TestCase):
    def test_page_link(self):
        block = customblock_factories.WagtailLinkBlockFactory(page_link=True)
        WagtailLinkBlock().clean(block)

        # Assert that choice is correct
        self.assertTrue(block["link_to"], ("page", _("Page")))

        # Assert that the page link is a page and that it is correct
        page = block["page"]
        self.assertIsNotNone(page)
        self.assertTrue(isinstance(page, Page))
        default_locale = Locale.get_default()
        self.assertEqual(page.locale, default_locale)

        # Assert that other fields are empty
        self.assertIsNone(block["file"])
        self.assertEqual(block["custom_url"], "")
        self.assertEqual(block["anchor"], "")
        self.assertEqual(block["email"], "")
        self.assertEqual(block["phone"], "")

        # Assert that `get_url` returns the correct URL
        self.assertEqual(block.get_url(), page.url)

    def test_document_link(self):
        block = customblock_factories.WagtailLinkBlockFactory(document_link=True)
        WagtailLinkBlock().clean(block)

        # Assert that choice is correct
        self.assertTrue(block["link_to"], ("document", _("Document")))

        # Assert that the document link is a document and that it is correct
        document = block["file"]
        self.assertIsNotNone(document)
        self.assertTrue(isinstance(document, Document))

        # Assert that other fields are empty
        self.assertIsNone(block["page"])
        self.assertEqual(block["custom_url"], "")
        self.assertEqual(block["anchor"], "")
        self.assertEqual(block["email"], "")
        self.assertEqual(block["phone"], "")

        # Assert that `get_url` returns the correct URL
        self.assertEqual(block.get_url(), document.url)

    def test_external_url_link(self):
        block = customblock_factories.WagtailLinkBlockFactory(external_url_link=True)
        WagtailLinkBlock().clean(block)

        # Assert that choice is correct
        self.assertTrue(block["link_to"], ("custom_url", _("External URL")))

        # Assert that the URL is a URL
        url = block["custom_url"]
        self.assertIsNotNone(url)

        # Assert that other fields are empty
        self.assertIsNone(block["page"])
        self.assertIsNone(block["file"])
        self.assertEqual(block["anchor"], "")
        self.assertEqual(block["email"], "")
        self.assertEqual(block["phone"], "")

        # Assert that `get_url` returns the correct URL
        self.assertEqual(block.get_url(), url)

    def test_anchor_link(self):
        block = customblock_factories.WagtailLinkBlockFactory(anchor_link=True)
        WagtailLinkBlock().clean(block)

        # Assert that choice is correct
        self.assertTrue(block["link_to"], ("anchor", _("Anchor")))

        # Assert that the anchor is an anchor
        anchor = block["anchor"]
        self.assertNotEqual(anchor, "")

        # Assert that other fields are empty
        self.assertIsNone(block["page"])
        self.assertIsNone(block["file"])
        self.assertEqual(block["custom_url"], "")
        self.assertEqual(block["email"], "")
        self.assertEqual(block["phone"], "")

        # Assert that `get_url` returns the correct URL
        self.assertEqual(block.get_url(), f"#{anchor}")

    def test_email_link(self):
        block = customblock_factories.WagtailLinkBlockFactory(email_link=True)
        WagtailLinkBlock().clean(block)

        # Assert that choice is correct
        self.assertTrue(block["link_to"], ("email", _("Email")))

        # Assert that the email is an email
        email = block["email"]
        self.assertNotEqual(email, "")

        # Assert that other fields are empty
        self.assertIsNone(block["page"])
        self.assertIsNone(block["file"])
        self.assertEqual(block["custom_url"], "")
        self.assertEqual(block["anchor"], "")
        self.assertEqual(block["phone"], "")

        # Assert that `get_url` returns the correct URL
        self.assertEqual(block.get_url(), f"mailto:{email}")

    def test_phone_link(self):
        block = customblock_factories.WagtailLinkBlockFactory(phone_link=True)
        WagtailLinkBlock().clean(block)

        # Assert that choice is correct
        self.assertTrue(block["link_to"], ("phone", _("Phone")))

        # Assert that the phone is a phone
        phone = block["phone"]
        self.assertNotEqual(phone, "")

        # Assert that other fields are empty
        self.assertIsNone(block["page"])
        self.assertIsNone(block["file"])
        self.assertEqual(block["custom_url"], "")
        self.assertEqual(block["anchor"], "")
        self.assertEqual(block["email"], "")

        # Assert that `get_url` returns the correct URL
        self.assertEqual(block.get_url(), f"tel:{phone}")

    def test_new_window(self):
        block = customblock_factories.WagtailLinkBlockFactory(page_link=True, new_window=True)

        # Assert that new_window is True
        self.assertTrue(block["new_window"])

    def test_needs_to_provide_at_least_one_link(self):
        with self.assertRaises(StreamBlockValidationError):
            block = customblock_factories.WagtailLinkBlockFactory()
            WagtailLinkBlock().clean(block)


class TestLinkBlock(TestCase):
    def test_default(self):
        """Assert that default LinkBlock factory works and is an external URL."""
        block = customblock_factories.LinkBlockFactory()

        # Assert that the page link is custom URL and that it is correct
        link = block["link"]
        url = link["custom_url"]
        self.assertEqual(link.get_url(), url)

    def test_page_link(self):
        """Create a LinkBlock with a page link."""
        block = customblock_factories.LinkBlockFactory(page_link=True)

        link = block["link"]
        page = link["page"]
        self.assertIsNotNone(page)
        self.assertTrue(isinstance(page, Page))
        self.assertEqual(link.get_url(), page.url)

    def test_document_link(self):
        """Create a LinkBlock with a file link."""
        block = customblock_factories.LinkBlockFactory(document_link=True)

        link = block["link"]
        document = link["file"]
        self.assertIsNotNone(document)
        self.assertTrue(isinstance(document, Document))
        self.assertEqual(link.get_url(), document.url)

    def test_external_url_link(self):
        """Create a LinkBlock with a custom/external URL."""
        block = customblock_factories.LinkBlockFactory(external_url_link=True)

        link = block["link"]
        url = link["custom_url"]
        self.assertIsNotNone(url)
        self.assertEqual(link.get_url(), url)

    def test_anchor_link(self):
        """Create a LinkBlock with an anchor link."""
        block = customblock_factories.LinkBlockFactory(anchor_link=True)

        link = block["link"]
        anchor = link["anchor"]
        self.assertNotEqual(anchor, "")
        self.assertEqual(link.get_url(), f"#{anchor}")

    def test_email_link(self):
        """Create a LinkBlock with an email link."""
        block = customblock_factories.LinkBlockFactory(email_link=True)

        link = block["link"]
        email = link["email"]
        self.assertNotEqual(email, "")
        self.assertEqual(link.get_url(), f"mailto:{email}")

    def test_phone_link(self):
        """Create a LinkBlock with a phone link."""
        block = customblock_factories.LinkBlockFactory(phone_link=True)

        link = block["link"]
        phone = link["phone"]
        self.assertNotEqual(phone, "")
        self.assertEqual(link.get_url(), f"tel:{phone}")

    def test_new_window(self):
        """Create a LinkBlock with new_window set to True."""
        block = customblock_factories.LinkBlockFactory(link__new_window=True)

        link = block["link"]
        self.assertTrue(link["new_window"])
