from django.test import SimpleTestCase

from foundation_cms.blocks.text_image_block import TextMediaBlock


class TextMediaBlockTests(SimpleTestCase):
    def test_form_layout_only_references_defined_child_blocks(self):
        block = TextMediaBlock()

        self.assertNotIn("image", block.child_blocks)
        self.assertEqual(block.meta.form_layout.children, list(block.child_blocks))
