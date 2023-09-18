from django.test import TestCase

from networkapi.wagtailpages.factory import customblocks as customblock_factories


class TestBlogCTACardWithTextBlock(TestCase):
    def test_blog_cta_card_with_text(self):
        card = customblock_factories.BlogCTACardWithTextBlockFactory(
            card__title="Test Title",
            alignment="left",
            paragraph="Test paragraph",
        )

        self.assertEqual(card["card"]["title"], "Test Title")
        self.assertEqual(card["alignment"], "left")
        self.assertEqual(card["paragraph"], "Test paragraph")
