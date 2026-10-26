from bs4 import BeautifulSoup
from django.template.loader import render_to_string
from django.test import SimpleTestCase
from wagtail.blocks import StreamBlock, StructBlockValidationError

from foundation_cms.base.models.abstract_base_page import BASE_BLOCK_NAMES
from foundation_cms.blocks.block_registry import BlockGroups, BlockRegistry
from foundation_cms.blocks.super_cta_block import SuperCTABlock


def raw_value(**overrides):
    return {
        "label": "Explore all our work",
        "link_to": "relative_url",
        "page": None,
        "external_url": "",
        "relative_url": "/our-work/",
        **overrides,
    }


class SuperCTABlockTests(SimpleTestCase):
    def render(self, **overrides):
        block = SuperCTABlock()
        value = block.to_python(raw_value(**overrides))
        return BeautifulSoup(block.render(value, context={"theme": "default"}), "html.parser")

    def test_whole_block_is_one_link_named_by_its_label(self):
        soup = self.render()

        links = soup.find_all("a")
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0]["href"], "/our-work/")
        self.assertEqual(links[0].get_text(strip=True), "Explore all our work")

    def test_arrows_are_hidden_from_assistive_technology(self):
        icons = self.render().select(".mzf-c-super-cta__icon")

        self.assertEqual(len(icons), 2)
        for icon in icons:
            self.assertEqual(icon["aria-hidden"], "true")

    def test_label_is_not_a_heading(self):
        soup = self.render()

        self.assertEqual(soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]), [])

    def test_links_to_an_external_url(self):
        soup = self.render(link_to="external_url", external_url="https://example.com/", relative_url="")

        self.assertEqual(soup.a["href"], "https://example.com/")

    def test_offers_only_internal_and_external_links(self):
        choices = [value for value, _label in SuperCTABlock().child_blocks["link_to"].field.choices if value]

        self.assertEqual(choices, ["page", "external_url", "relative_url"])

    def test_label_is_required_and_capped_at_30_characters(self):
        block = SuperCTABlock()

        for label in ("", "x" * 31):
            with self.subTest(label=label), self.assertRaises(StructBlockValidationError):
                block.clean(block.to_python(raw_value(label=label)))

    def test_is_an_engagement_block_on_every_base_page(self):
        self.assertEqual(BlockRegistry.BLOCKS["super_cta"]["group"], BlockGroups.ENGAGEMENT)
        self.assertIn("super_cta", BASE_BLOCK_NAMES)

    def test_streamfield_renders_it_full_bleed(self):
        stream_block = StreamBlock(BlockRegistry.get_blocks(["super_cta"]))
        stream_value = stream_block.to_python([{"type": "super_cta", "value": raw_value()}])

        html = render_to_string("patterns/components/_streamfield.html", {"streamfield": stream_value})

        self.assertIn("mzf-c-super-cta", html)
        self.assertNotIn("grid-container", html)
