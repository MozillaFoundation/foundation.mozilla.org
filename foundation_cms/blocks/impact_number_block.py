from wagtail import blocks

from foundation_cms.base.models.base_block import BaseBlock

NUM_IMPACT_STATS = 3
DEFAULT_IMPACT_STATS = [{"stat_number": "", "stat_heading": ""} for _ in range(NUM_IMPACT_STATS)]


class ImpactStatBlock(blocks.StructBlock):

    stat_number = blocks.CharBlock(
        required=True,
        max_length=5,
        help_text=(
            "The figure, written the way it should be read aloud, including any symbols, "
            "commas, decimals, or suffixes (e.g., $5.2M)."
        ),
    )

    stat_heading = blocks.CharBlock(required=True, help_text="The line that says what the number counts")

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
