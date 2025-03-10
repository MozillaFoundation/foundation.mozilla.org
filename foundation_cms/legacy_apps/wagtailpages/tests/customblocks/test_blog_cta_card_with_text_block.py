from django.test import TestCase
from wagtail.blocks.struct_block import StructBlockValidationError
from wagtail.rich_text import RichText

from foundation_cms.legacy_apps.wagtailpages.factory import (
    customblocks as customblock_factories,
)
from foundation_cms.legacy_apps.wagtailpages.pagemodels import (
    customblocks as customblock_models,
)


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

    def test_paragraph_text_cannot_be_shorter_than_card_content(self):
        card_value = customblock_factories.BlogCTACardWithTextBlockFactory(
            card__title="1",
            card__body=RichText("<p>2</p>"),
            paragraph=RichText("<p>1</p>"),
        )

        card = customblock_models.BlogCTACardWithTextBlock()

        # Paragraph has only 1 character, while card has 2 (1 in title and 1 in body)
        with self.assertRaises(StructBlockValidationError):
            card.clean(card_value)

    def test_paragraph_text_can_be_longer_than_card_content(self):
        card_value = customblock_factories.BlogCTACardWithTextBlockFactory(
            card__title="A title",
            card__body=RichText("<p>A body</p>"),
            paragraph=RichText("<p>A body longer than the card's title and body!</p>"),
        )

        card = customblock_models.BlogCTACardWithTextBlock()

        cleaned_data = card.clean(card_value)
        self.assertEqual(cleaned_data["card"]["title"], "A title")
