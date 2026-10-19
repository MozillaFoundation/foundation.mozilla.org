from bs4 import BeautifulSoup
from django.test import SimpleTestCase
from wagtail.blocks import StreamBlockValidationError, StructBlockValidationError

from foundation_cms.blocks.block_registry import BlockRegistry
from foundation_cms.blocks.meet_mozilla_block import MeetMozillaBlock
from foundation_cms.core.models.home_page import HomePage

STEPS = [
    {"label": "Imagine", "statement": "We search in unlikely places."},
    {"label": "Co-create", "statement": "We offer capital and expertise."},
    {"label": "Mobilize", "statement": "We connect builders and dreamers."},
]


def link(**overrides):
    return {
        "label": "Learn more",
        "link_to": "external_url",
        "page": None,
        "external_url": "https://example.com",
        "relative_url": "",
        "anchor": "",
        "email": "",
        "file": None,
        "phone": "",
        "new_window": False,
        **overrides,
    }


def raw_value(**overrides):
    return {
        "eyebrow": "Meet Mozilla",
        "heading": "We back what others overlook.",
        "intro": "Advancing technology that reflects human values.",
        "intro_link": [],
        "steps": STEPS,
        **overrides,
    }


class MeetMozillaBlockTests(SimpleTestCase):
    def value(self, **overrides):
        return MeetMozillaBlock().to_python(raw_value(**overrides))

    def render(self, **overrides):
        html = MeetMozillaBlock().render(self.value(**overrides), context={"theme": "default"})
        return BeautifulSoup(html, "html.parser")

    def test_renders_the_heading_outline(self):
        soup = self.render()

        self.assertEqual(soup.select_one(".mzf-c-text-group__label").get_text(), "Meet Mozilla")
        self.assertEqual(soup.select_one("h2").get_text(), "We back what others overlook.")
        self.assertEqual(
            [h3.get_text() for h3 in soup.select("h3")],
            [
                "Advancing technology that reflects human values.",
                "We search in unlikely places.",
                "We offer capital and expertise.",
                "We connect builders and dreamers.",
            ],
        )

    def test_omits_the_eyebrow_when_empty(self):
        soup = self.render(eyebrow="")

        self.assertIsNone(soup.select_one(".mzf-c-text-group__label"))

    def test_numbers_steps_by_position(self):
        soup = self.render()

        self.assertEqual([n.get_text() for n in soup.select("ol .mzf-c-big-label__number")], ["01", "02", "03"])
        self.assertEqual(
            [label.get_text() for label in soup.select("ol .mzf-c-big-label__label")],
            ["Imagine", "Co-create", "Mobilize"],
        )

    def test_starts_on_the_first_state(self):
        root = self.render().select_one(".mzf-c-meet-mozilla")

        self.assertIn("mzf-c-meet-mozilla--state-00", root["class"])
        self.assertTrue(root.has_attr("data-mzf-meet-mozilla"))

    def test_fourth_step_carries_no_state(self):
        soup = self.render(steps=STEPS + [{"label": "Repeat", "statement": "And again."}])

        self.assertEqual(
            [item.get("data-mzf-meet-mozilla-state") for item in soup.select(".mzf-c-meet-mozilla__item")],
            ["01", "02", "03", None],
        )

    def test_renders_the_optional_intro_link(self):
        soup = self.render(intro_link=[link(new_window=True)])

        anchor = soup.select_one(".mzf-c-text-group--action-link a.mzf-c-link--primary")
        self.assertEqual(anchor["href"], "https://example.com")
        self.assertEqual(anchor["target"], "_blank")
        self.assertEqual(anchor.get_text(strip=True), "Learn more")

    def test_leaves_out_the_action_slot_without_a_link(self):
        soup = self.render()

        self.assertIsNone(soup.select_one(".mzf-c-text-group--action-link"))
        self.assertIsNone(soup.select_one(".mzf-c-link"))

    def test_escapes_editor_supplied_text(self):
        html = str(self.render(heading="<script>alert('x')</script>"))

        self.assertNotIn("<script>", html)

    def test_requires_three_to_four_steps(self):
        block = MeetMozillaBlock()

        for steps in (STEPS[:2], STEPS + STEPS[:2]):
            with self.subTest(count=len(steps)):
                with self.assertRaises(StructBlockValidationError) as raised:
                    block.clean(self.value(steps=steps))

                self.assertEqual(list(raised.exception.block_errors), ["steps"])


class MeetMozillaHomePageTests(SimpleTestCase):
    def test_is_a_fixed_homepage_field_not_a_body_block(self):
        field = HomePage._meta.get_field("meet_mozilla")

        self.assertEqual(list(field.stream_block.child_blocks), ["meet_mozilla"])
        self.assertNotIn("meet_mozilla", HomePage._meta.get_field("body").stream_block.child_blocks)
        self.assertNotIn("meet_mozilla", BlockRegistry.BLOCKS)

    def test_homepage_allows_one(self):
        stream_block = HomePage._meta.get_field("meet_mozilla").stream_block
        one = [{"type": "meet_mozilla", "value": raw_value()}]

        stream_block.clean(stream_block.to_python(one))

        with self.assertRaises(StreamBlockValidationError) as raised:
            stream_block.clean(stream_block.to_python(one * 2))

        self.assertFalse(raised.exception.block_errors)
        self.assertIn("maximum number of items is 1", str(raised.exception.non_block_errors))
