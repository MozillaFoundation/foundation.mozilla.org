from django.test import SimpleTestCase
from wagtail import blocks
from wagtail.blocks.definition_lookup import BlockDefinitionLookupBuilder

from foundation_cms.blocks.common.limited_list_block import LimitedListBlock


class TestLimitedListBlock(SimpleTestCase):
    def test_attaches_the_list_limit_controller_with_its_limits(self):
        block = LimitedListBlock(blocks.CharBlock(), min_num=2, max_num=4)

        self.assertEqual(
            block.meta.form_attrs,
            {
                "data-controller": "list-limit",
                "data-list-limit-min-value": "2",
                "data-list-limit-max-value": "4",
            },
        )

    def test_min_defaults_to_zero(self):
        block = LimitedListBlock(blocks.CharBlock(), max_num=4)

        self.assertEqual(block.meta.form_attrs["data-list-limit-min-value"], "0")

    def test_migrates_as_a_plain_list_block(self):
        limited = LimitedListBlock(blocks.CharBlock(), min_num=2, max_num=4)
        plain = blocks.ListBlock(blocks.CharBlock(), min_num=2, max_num=4)

        self.assertEqual(
            limited.deconstruct_with_lookup(BlockDefinitionLookupBuilder()),
            plain.deconstruct_with_lookup(BlockDefinitionLookupBuilder()),
        )
