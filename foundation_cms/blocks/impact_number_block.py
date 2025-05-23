# blocks.py
from wagtail import blocks

from foundation_cms.base.models.base_block import BaseBlock


class ImpactStatBlock(blocks.StructBlock):
    stat_number = blocks.IntegerBlock(required=True, help_text="The number to count up to")
    stat_description = blocks.CharBlock(required=True, help_text="Short description of the stat")

    class Meta:
        icon = "plus"
        label = "Impact Stat"


class ImpactNumberBlock(BaseBlock):
    stats = blocks.ListBlock(
        ImpactStatBlock(),
        min_num=1,
        max_num=3,
        label="Impact Stats",
        help_text="Add 1 to 3 stats to appear in the Impact Numbers section",
    )

    class Meta:
        template_name = "impact_number_block.html"
        icon = "form"
        label = "Impact Numbers"
