from wagtail import blocks

from foundation_cms.base.models.base_block import BaseBlock
from foundation_cms.blocks.block_registry import BlockRegistry

# Deliberately conservative prototype allowlist. Full-width and singleton
# engagement blocks remain page-level until their layout and validation is audited.
SECTION_BLOCK_NAMES = [
    "rich_text",
    "title_block",
    "quote",
    "link_button_block",
    "image",
    "image_grid",
    "accordion_block",
    "list_block",
    "two_column_container_block",
    "three_column_container_block",
]


class SectionMasterBlock(BaseBlock):
    label = blocks.CharBlock(required=False, help_text="Editor-only section label.")
    padding = blocks.ChoiceBlock(
        choices=[("none", "None"), ("regular", "Regular"), ("generous", "Generous")],
        default="regular",
    )
    rhythm = blocks.ChoiceBlock(
        choices=[("compact", "Compact"), ("regular", "Regular"), ("relaxed", "Relaxed")],
        default="regular",
    )
    content = blocks.StreamBlock(BlockRegistry.get_blocks(SECTION_BLOCK_NAMES), required=False)

    class Meta:
        template_name = "section_master_block.html"
        icon = "folder-open-inverse"
        label = "Section Master"
        label_format = "{label}"
