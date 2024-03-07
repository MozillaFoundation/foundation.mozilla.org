from django.test import TestCase
from wagtail.documents.models import Document
from wagtail.models import Page

from networkapi.wagtailpages.factory import customblocks as customblock_factories


class TestLinkButtonBlock(TestCase):
    def test_default(self):
        """Assert that default LinkButtonBlockFactory works and is an external URL."""
        block = customblock_factories.LinkButtonBlockFactory()

        # Assert that the page link is custom URL and that it is correct
        link = block["link"]
        url = link["custom_url"]
        self.assertEqual(link.get_url(), url)

    def test_page_link(self):
        """Create a LinkButtonBlockFactory with a page link."""
        block = customblock_factories.LinkButtonBlockFactory(page_link=True)

        link = block["link"]
        page = link["page"]
        self.assertIsNotNone(page)
        self.assertTrue(isinstance(page, Page))
        self.assertEqual(link.get_url(), page.url)

    def test_document_link(self):
        """Create a LinkButtonBlockFactory with a file link."""
        block = customblock_factories.LinkButtonBlockFactory(document_link=True)

        link = block["link"]
        document = link["file"]
        self.assertIsNotNone(document)
        self.assertTrue(isinstance(document, Document))
        self.assertEqual(link.get_url(), document.url)

    def test_external_url_link(self):
        """Create a LinkButtonBlockFactory with a custom/external URL."""
        block = customblock_factories.LinkButtonBlockFactory(external_url_link=True)

        link = block["link"]
        url = link["custom_url"]
        self.assertIsNotNone(url)
        self.assertEqual(link.get_url(), url)

    def test_anchor_link(self):
        """Create a LinkButtonBlockFactory with an anchor link."""
        block = customblock_factories.LinkButtonBlockFactory(anchor_link=True)

        print(block)

        link = block["link"]
        anchor = link["anchor"]
        self.assertNotEqual(anchor, "")
        self.assertEqual(link.get_url(), f"#{anchor}")

    def test_email_link(self):
        """Create a LinkButtonBlockFactory with an email link."""
        block = customblock_factories.LinkButtonBlockFactory(email_link=True)

        link = block["link"]
        email = link["email"]
        self.assertNotEqual(email, "")
        self.assertEqual(link.get_url(), f"mailto:{email}")

    def test_phone_link(self):
        """Create a LinkButtonBlockFactory with a phone link."""
        block = customblock_factories.LinkButtonBlockFactory(phone_link=True)

        link = block["link"]
        phone = link["phone"]
        self.assertNotEqual(phone, "")
        self.assertEqual(link.get_url(), f"tel:{phone}")

    def test_new_window(self):
        """Create a LinkButtonBlockFactory with new_window set to True."""
        block = customblock_factories.LinkButtonBlockFactory(new_window=True)

        self.assertTrue(block["new_window"])

    def test_styling(self):
        """Create a LinkButtonBlock with a styling."""
        block = customblock_factories.LinkButtonBlockFactory(styling="btn-primary")

        self.assertEqual(block["styling"], "btn-primary")
