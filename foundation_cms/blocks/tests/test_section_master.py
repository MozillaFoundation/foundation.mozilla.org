from copy import deepcopy

from django.test import SimpleTestCase

from foundation_cms.blocks.section_master_block import SectionMasterBlock
from foundation_cms.blocks.section_master_migration import (
    unwrap_sections,
    wrap_sections,
)
from foundation_cms.core.models import GeneralPage


class SectionMasterTests(SimpleTestCase):
    def test_mixed_content_roundtrip_and_idempotence(self):
        body = [
            {"type": "rich_text", "id": "a", "value": "<p>A</p>"},
            {"type": "rich_text", "id": "b", "value": "<p>B</p>"},
            {"type": "divider", "id": "divider", "value": {}},
            {"type": "rich_text", "id": "c", "value": "<p>C</p>"},
            {"type": "custom_media", "id": "wide", "value": {"orientation": "widescreen"}},
            {"type": "donor_help_contact_us_form", "id": "form", "value": {"heading": "Contact"}},
            {"type": "future_block", "id": "unknown", "value": {"opaque": [1, 2]}},
            {"type": "rich_text", "value": "<p>No ID: leave unchanged</p>"},
        ]
        snapshot = deepcopy(body)
        wrapped = wrap_sections(body)
        self.assertEqual(
            [b["type"] for b in wrapped],
            [
                "section_master",
                "divider",
                "section_master",
                "custom_media",
                "donor_help_contact_us_form",
                "future_block",
                "rich_text",
            ],
        )
        self.assertEqual(wrapped[0]["value"]["content"], body[:2])
        self.assertEqual(wrap_sections(wrapped), wrapped)
        ids = {b["id"] for b in wrapped if b["type"] == "section_master"}
        self.assertEqual(unwrap_sections(wrapped, ids), body)
        self.assertEqual(body, snapshot)

    def test_reverse_preserves_manual_sections(self):
        manual = {"type": "section_master", "id": "manual", "value": {"content": []}}
        body = [manual, {"type": "rich_text", "id": "a", "value": "<p>A</p>"}]
        wrapped = wrap_sections(body)
        self.assertEqual(unwrap_sections(wrapped, {wrapped[1]["id"]}), body)

    def test_roundtrip_through_streamfield_keeps_child_ids(self):
        body = [{"type": "rich_text", "id": "a", "value": "<p>A</p>"}]
        field = GeneralPage._meta.get_field("body")
        wrapped = wrap_sections(body)
        self.assertEqual(field.get_prep_value(field.to_python(wrapped)), wrapped)

    def test_label_is_editor_only_and_forms_are_excluded(self):
        block = SectionMasterBlock()
        value = block.to_python(
            {
                "label": "Private editorial label",
                "padding": "generous",
                "rhythm": "compact",
                "content": [{"type": "rich_text", "id": "a", "value": "<p>Visible content</p>"}],
            }
        )
        html = block.render(value, context={"theme": "default"})
        self.assertNotIn("Private editorial label", html)
        self.assertIn("Visible content", html)
        self.assertIn("section-master--padding-generous", html)
        self.assertNotIn("donor_help_contact_us_form", block.child_blocks["content"].child_blocks)
        self.assertNotIn("greenhouse_board", block.child_blocks["content"].child_blocks)
