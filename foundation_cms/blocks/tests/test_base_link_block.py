import wagtail_factories
from django.test import TestCase
from wagtail.blocks import StreamBlockValidationError

from foundation_cms.blocks.factories import LinkBlockFactory
from foundation_cms.blocks.link_block import LinkBlock


class TestBaseLinkBlockClean(TestCase):
    def test_valid_external_url_clears_stale_values(self):
        """A valid external_url link should pass validation and clear other link-target fields."""
        block = LinkBlockFactory(
            link_to="external_url",
            external_url="https://example.com",
            page=None,
            relative_url="/stale/",
        )

        result = LinkBlock().clean(block)

        self.assertEqual(result["external_url"], "https://example.com")
        self.assertIsNone(result["page"])
        self.assertEqual(result["relative_url"], "")

    def test_valid_page_link_clears_stale_values(self):
        """A valid page link should pass validation and clear other link-target fields."""
        page = wagtail_factories.PageFactory()
        block = LinkBlockFactory(link_to="page", page=page, external_url="https://stale.example.com")

        result = LinkBlock().clean(block)

        self.assertEqual(result["page"], page)
        self.assertEqual(result["external_url"], "")

    def test_invalid_missing_target_for_chosen_link_type(self):
        """Choosing a link type without a value for it should fail validation."""
        block = LinkBlockFactory(link_to="external_url", external_url="")

        with self.assertRaises(StreamBlockValidationError) as cm:
            LinkBlock().clean(block)

        self.assertEqual(
            cm.exception.block_errors["external_url"].message,
            "You need to add a external url link",
        )
