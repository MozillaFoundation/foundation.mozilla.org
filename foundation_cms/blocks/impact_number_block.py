# blocks.py
from wagtail import blocks

from foundation_cms.base.models.base_block import BaseBlock

NUM_IMPACT_STATS = 3
DEFAULT_IMPACT_STATS = [
    {"stat_number": "", "stat_heading": "", "stat_description": ""} for _ in range(NUM_IMPACT_STATS)
]


class ImpactStatBlock(blocks.StructBlock):

    stat_number = blocks.CharBlock(
        required=True,
        max_length=5,
        help_text="The full value to animate, including any symbols, commas, decimals, or suffixes (e.g., $5.2M).",
    )

    stat_heading = blocks.CharBlock(required=True, help_text="Heading of the stat")
    stat_description = blocks.CharBlock(required=True, help_text="Short description of the stat")

    class Meta:
        icon = "plus"
        label = "Impact Stat"


class ImpactNumberBlock(BaseBlock):
    stats = blocks.ListBlock(
        ImpactStatBlock(),
        min_num=NUM_IMPACT_STATS,
        max_num=NUM_IMPACT_STATS,
        default=DEFAULT_IMPACT_STATS,
        label="Impact Stats",
        help_text="Add exactly 3 stats to appear in the Impact Numbers section",
    )

    class Meta:
        template_name = "impact_number_block.html"
        icon = "form"
        label = "Impact Numbers"
