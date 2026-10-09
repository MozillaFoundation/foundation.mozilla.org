from pathlib import Path

from bs4 import BeautifulSoup
from django.template.loader import render_to_string
from django.test import SimpleTestCase
from wagtail.blocks import StreamBlock, StructBlockValidationError

from foundation_cms.base.models.abstract_base_page import BASE_BLOCK_NAMES
from foundation_cms.blocks.block_registry import BlockGroups, BlockRegistry
from foundation_cms.blocks.flywheel_banner_block import (
    MISSION_CHOICES,
    FlywheelBannerBlock,
)

ASSET_DIRECTORY = Path(__file__).parents[2] / "static" / "images" / "flywheel_banner"


class FlywheelBannerBlockTests(SimpleTestCase):
    def render(self, **overrides):
        block = FlywheelBannerBlock()
        value = block.to_python(
            {
                "mission": "imagine",
                "heading": "Imagine",
                **overrides,
            }
        )
        return block.render(value, context={"theme": "default"})

    def test_defaults_to_the_imagine_mission(self):
        value = FlywheelBannerBlock().get_default()

        self.assertEqual(value["mission"], "imagine")
        self.assertEqual(value["heading"], "Imagine")

    def test_offers_all_three_missions(self):
        choices = list(FlywheelBannerBlock().child_blocks["mission"].field.choices)

        self.assertEqual(choices, MISSION_CHOICES)

    def test_heading_is_required(self):
        block = FlywheelBannerBlock()

        with self.assertRaises(StructBlockValidationError):
            block.clean(block.to_python({"mission": "imagine", "heading": ""}))

    def test_renders_live_heading_and_decorative_artwork(self):
        soup = BeautifulSoup(self.render(), "html.parser")

        self.assertEqual(soup.select_one("h2.flywheel-banner__heading").get_text(), "Imagine")
        artwork = soup.select_one(".flywheel-banner__artwork")
        self.assertEqual(artwork["aria-hidden"], "true")
        self.assertFalse(artwork.get_text(strip=True))

    def test_applies_the_selected_mission_variant(self):
        soup = BeautifulSoup(self.render(mission="co-create", heading="Mitgestalten"), "html.parser")

        self.assertIsNotNone(soup.select_one(".flywheel-banner--co-create"))
        self.assertEqual(soup.select_one(".flywheel-banner__heading").get_text(), "Mitgestalten")

    def test_escapes_editor_supplied_heading(self):
        html = self.render(heading="<script>alert('x')</script>")

        self.assertNotIn("<script>", html)
        self.assertIn("&lt;script&gt;", html)

    def test_is_registered_as_a_full_bleed_base_block(self):
        block_info = BlockRegistry.BLOCKS["flywheel_banner"]

        self.assertEqual(block_info["group"], BlockGroups.BANNERS)
        self.assertTrue(block_info["class"](**block_info["kwargs"]).skip_default_wrapper)
        self.assertIn("flywheel_banner", BASE_BLOCK_NAMES)

    def test_streamfield_does_not_add_the_grid_wrapper(self):
        stream_block = StreamBlock(BlockRegistry.get_blocks(["flywheel_banner"]))
        stream_value = stream_block.to_python(
            [{"type": "flywheel_banner", "value": {"mission": "imagine", "heading": "Imagine"}}]
        )

        html = render_to_string("patterns/components/_streamfield.html", {"streamfield": stream_value})

        self.assertIn('data-block-type="flywheel_banner"', html)
        self.assertNotIn("grid-container", html)

    def test_each_mission_has_nonempty_static_artwork(self):
        for mission, _label in MISSION_CHOICES:
            with self.subTest(mission=mission):
                artwork = ASSET_DIRECTORY / f"{mission}.png"

                self.assertTrue(artwork.is_file())
                self.assertGreater(artwork.stat().st_size, 0)
