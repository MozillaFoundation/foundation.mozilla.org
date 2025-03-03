from django.test import TestCase
from wagtail.blocks import StreamBlockValidationError
from wagtail.documents.models import Document
from wagtail.models import Locale, Page

from foundation_cms.legacy_cms.wagtailpages.factory import customblocks as customblock_factories
from foundation_cms.legacy_cms.wagtailpages.pagemodels.customblocks.link_block import LinkBlock


class TestLinkBlock(TestCase):
    def test_default(self):
        """Assert that default LinkBlock factory works and is an external URL."""
        block = customblock_factories.LinkBlockFactory()

        # Assert that the page link is custom URL and that it is correct
        url = block["external_url"]
        self.assertEqual(block.url, url)

    def test_page_link(self):
        """Create a LinkBlock with a page link."""
        block = customblock_factories.LinkBlockFactory(page_link=True)

        page = block["page"]
        self.assertIsNotNone(page)
        self.assertTrue(isinstance(page, Page))
        default_locale = Locale.get_default()
        self.assertEqual(page.locale, default_locale)

        # Assert that other fields are empty
        self.assertIsNone(block["file"])
        self.assertEqual(block["external_url"], "")
        self.assertEqual(block["relative_url"], "")
        self.assertEqual(block["anchor"], "")
        self.assertEqual(block["email"], "")
        self.assertEqual(block["phone"], "")

    def test_document_link(self):
        """Create a LinkBlock with a file link."""
        block = customblock_factories.LinkBlockFactory(document_link=True)

        # Assert that the document link is a document and that it is correct
        document = block["file"]
        self.assertIsNotNone(document)
        self.assertTrue(isinstance(document, Document))

        # Assert that other fields are empty
        self.assertIsNone(block["page"])
        self.assertEqual(block["external_url"], "")
        self.assertEqual(block["relative_url"], "")
        self.assertEqual(block["anchor"], "")
        self.assertEqual(block["email"], "")
        self.assertEqual(block["phone"], "")

    def test_external_url_link(self):
        """Create a LinkBlock with a custom/external URL."""
        block = customblock_factories.LinkBlockFactory(external_url_link=True)

        # Assert that the URL is a URL
        url = block["external_url"]
        self.assertIsNotNone(url)

        # Assert that other fields are empty
        self.assertIsNone(block["page"])
        self.assertIsNone(block["file"])
        self.assertEqual(block["relative_url"], "")
        self.assertEqual(block["anchor"], "")
        self.assertEqual(block["email"], "")
        self.assertEqual(block["phone"], "")

    def test_relative_url_link(self):
        """Create a LinkBlock with a relative URL."""
        block = customblock_factories.LinkBlockFactory(relative_url_link=True)

        # Assert that the URL is a URL
        url = block["relative_url"]
        self.assertIsNotNone(url)

        # Assert that other fields are empty
        self.assertIsNone(block["page"])
        self.assertIsNone(block["file"])
        self.assertEqual(block["external_url"], "")
        self.assertEqual(block["anchor"], "")
        self.assertEqual(block["email"], "")
        self.assertEqual(block["phone"], "")

    def test_anchor_link(self):
        """Create a LinkBlock with an anchor link."""
        block = customblock_factories.LinkBlockFactory(anchor_link=True)

        # Assert that the anchor is an anchor
        anchor = block["anchor"]
        self.assertNotEqual(anchor, "")

        # Assert that other fields are empty
        self.assertIsNone(block["page"])
        self.assertIsNone(block["file"])
        self.assertEqual(block["external_url"], "")
        self.assertEqual(block["relative_url"], "")
        self.assertEqual(block["email"], "")
        self.assertEqual(block["phone"], "")

    def test_email_link(self):
        """Create a LinkBlock with an email link."""
        block = customblock_factories.LinkBlockFactory(email_link=True)

        # Assert that the email is an email
        email = block["email"]
        self.assertNotEqual(email, "")

        # Assert that other fields are empty
        self.assertIsNone(block["page"])
        self.assertIsNone(block["file"])
        self.assertEqual(block["external_url"], "")
        self.assertEqual(block["relative_url"], "")
        self.assertEqual(block["anchor"], "")
        self.assertEqual(block["phone"], "")

    def test_phone_link(self):
        """Create a LinkBlock with a phone link."""
        block = customblock_factories.LinkBlockFactory(phone_link=True)

        # Assert that the phone is a phone
        phone = block["phone"]
        self.assertNotEqual(phone, "")

        # Assert that other fields are empty
        self.assertIsNone(block["page"])
        self.assertIsNone(block["file"])
        self.assertEqual(block["external_url"], "")
        self.assertEqual(block["relative_url"], "")
        self.assertEqual(block["anchor"], "")
        self.assertEqual(block["email"], "")

    def test_new_window(self):
        """Create a LinkBlock with new_window set to True."""
        block = customblock_factories.LinkBlockFactory(new_window=True)

        self.assertTrue(block["new_window"])

    def test_needs_to_provide_at_least_one_link(self):
        with self.assertRaises(StreamBlockValidationError):
            block = customblock_factories.LinkBlockFactory()
            LinkBlock().clean(block)
