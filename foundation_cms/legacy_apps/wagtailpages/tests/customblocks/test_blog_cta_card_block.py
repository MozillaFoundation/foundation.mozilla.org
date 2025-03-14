from django.test import TestCase

from foundation_cms.legacy_apps.wagtailpages.factory import (
    customblocks as customblock_factories,
)


class TestBlogCTACardBlock(TestCase):
    def test_blog_cta_card_all_optionals(self):
        full_card = customblock_factories.BlogCTACardBlockFactory()
        self.assertIsNotNone(full_card["title"])
        self.assertIsNotNone(full_card["image"])
        self.assertIsNotNone(full_card["button"])

    def test_blog_cta_card_no_optionals(self):
        no_optionals_card = customblock_factories.BlogCTACardBlockFactory(no_title=True, no_image=True, no_button=True)
        self.assertIsNone(no_optionals_card["title"])
        self.assertEqual(no_optionals_card["image"], [])
        self.assertEqual(no_optionals_card["button"], [])

    def test_blog_cta_card_optional_elements(self):
        card = customblock_factories.BlogCTACardBlockFactory(
            title="Test Title",
            image__0__altText="Test alt text",
            button__0__label="Test label",
            button__0__URL="https://www.example.com",
            button__0__styling="btn-primary",
        )

        self.assertEqual(card["title"], "Test Title")
        self.assertIsNotNone(card["image"])
        self.assertEqual(card["image"][0]["altText"], "Test alt text")
        self.assertEqual(card["button"][0]["label"], "Test label")
        self.assertEqual(card["button"][0]["URL"], "https://www.example.com")
        self.assertEqual(card["button"][0]["styling"], "btn-primary")
