from django.test import SimpleTestCase
from wagtail import blocks

from foundation_cms.blocks.section_start_block import SectionStartBlock
from foundation_cms.blocks.sections import group_into_sections

stream_block = blocks.StreamBlock(
    [
        ("section_start", SectionStartBlock()),
        ("text", blocks.CharBlock()),
    ]
)


def marker(name, surface="default"):
    return {"type": "section_start", "value": {"name": name, "surface": surface, "anchor_id": ""}}


def text(value):
    return {"type": "text", "value": value}


def build_stream(*children):
    return stream_block.to_python(list(children))


def texts(section):
    return [child.value for child in section.blocks]


class TestGroupIntoSections(SimpleTestCase):
    def test_empty_stream(self):
        self.assertEqual(group_into_sections(build_stream()), [])
        self.assertEqual(group_into_sections(None), [])

    def test_no_markers_gives_one_implicit_section(self):
        sections = group_into_sections(build_stream(text("a"), text("b")))

        self.assertEqual(len(sections), 1)
        self.assertTrue(sections[0].is_implicit)
        self.assertEqual(texts(sections[0]), ["a", "b"])

    def test_blocks_before_first_marker_form_implicit_section(self):
        sections = group_into_sections(build_stream(text("intro"), marker("One"), text("a")))

        self.assertEqual(len(sections), 2)
        self.assertTrue(sections[0].is_implicit)
        self.assertEqual(texts(sections[0]), ["intro"])
        self.assertEqual(sections[1].settings["name"], "One")
        self.assertEqual(texts(sections[1]), ["a"])

    def test_each_marker_starts_a_new_section_in_order(self):
        sections = group_into_sections(
            build_stream(
                marker("One", surface="ground"),
                text("a"),
                text("b"),
                marker("Two"),
                text("c"),
            )
        )

        self.assertEqual([s.settings["name"] for s in sections], ["One", "Two"])
        self.assertEqual(sections[0].settings["surface"], "ground")
        self.assertEqual([texts(s) for s in sections], [["a", "b"], ["c"]])

    def test_marker_blocks_are_not_included_in_section_blocks(self):
        sections = group_into_sections(build_stream(marker("One"), text("a")))

        self.assertEqual([child.block_type for child in sections[0].blocks], ["text"])

    def test_consecutive_markers_drop_the_empty_section(self):
        sections = group_into_sections(build_stream(marker("Empty"), marker("One"), text("a")))

        self.assertEqual(len(sections), 1)
        self.assertEqual(sections[0].settings["name"], "One")

    def test_trailing_marker_is_dropped(self):
        sections = group_into_sections(build_stream(marker("One"), text("a"), marker("Trailing")))

        self.assertEqual(len(sections), 1)
        self.assertEqual(sections[0].settings["name"], "One")


class TestSectionStartBlock(SimpleTestCase):
    def test_renders_nothing_when_rendered_directly(self):
        value = SectionStartBlock().to_python({"name": "One", "surface": "default", "anchor_id": ""})

        self.assertEqual(SectionStartBlock().render(value), "")

    def test_anchor_id_must_be_a_slug(self):
        block = SectionStartBlock()

        with self.assertRaises(blocks.StructBlockValidationError):
            block.clean(block.to_python({"name": "One", "surface": "default", "anchor_id": "Not A Slug"}))

        block.clean(block.to_python({"name": "One", "surface": "default", "anchor_id": "get-involved"}))

    def test_spacing_defaults_to_lp_defaults_for_markers_saved_without_it(self):
        value = SectionStartBlock().to_python({"name": "One", "surface": "default", "anchor_id": ""})

        self.assertEqual(value["rhythm"], "xlarge")
        self.assertEqual(value["padding"], "large")

    def test_name_is_required(self):
        block = SectionStartBlock()

        with self.assertRaises(blocks.StructBlockValidationError):
            block.clean(block.to_python({"name": "", "surface": "default", "anchor_id": ""}))
