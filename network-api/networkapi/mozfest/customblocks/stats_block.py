from wagtail import blocks


class StatisticCard(blocks.StructBlock):
    title = blocks.CharBlock(help_text="The statistic figure, e.g '1000+' or '10%'")
    description = blocks.CharBlock(help_text="Context or description for the statistic")


class MozfestStatisticsBlock(blocks.StructBlock):
    statistics = blocks.ListBlock(StatisticCard(), help_text="Please use a minimum of 2 cards.")

    class Meta:
        icon = "placeholder"
        template = "fragments/blocks/mozfest_stats_block.html"
        label = "Mozfest Stats Block"
