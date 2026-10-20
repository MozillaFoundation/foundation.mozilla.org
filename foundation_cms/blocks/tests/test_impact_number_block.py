from bs4 import BeautifulSoup
from django.test import SimpleTestCase

from foundation_cms.blocks.impact_number_block import ImpactNumberBlock, ImpactStatBlock

STATS = [
    {"stat_number": "$35M", "stat_heading": "In grants awarded to community-led projects"},
    {"stat_number": "6M+", "stat_heading": "People in the movement for a better tech future"},
    {"stat_number": "1M+", "stat_heading": "Voices donated to the Common Voice project"},
]


class TestImpactNumberBlock(SimpleTestCase):
    def render(self, stats):
        block = ImpactNumberBlock()
        return BeautifulSoup(block.render(block.to_python({"stats": stats})), "html.parser")

    def test_renders_one_statistic_card_per_stat_in_a_three_column_grid(self):
        soup = self.render(STATS)

        grid = soup.select_one("ul.mzf-c-card-grid.mzf-c-card-grid--columns-3")
        cards = grid.select("li.mzf-c-card-grid__item > .mzf-c-card.mzf-c-card--statistic")
        self.assertEqual(len(cards), 3)
        self.assertEqual(
            [card.select_one(".mzf-c-card__description").get_text(strip=True) for card in cards],
            [stat["stat_heading"] for stat in STATS],
        )

    def test_figure_is_announced_once_and_animated_from_the_hidden_copy(self):
        card = self.render(STATS).select_one("[data-impact-stat]")

        figure = card.select_one(".mzf-c-card__figure")
        self.assertEqual(figure.select_one(".show-for-sr").get_text(strip=True), "$35M")
        animated = figure.select_one("[data-impact-stat-count-up]")
        self.assertEqual(animated["aria-hidden"], "true")
        self.assertEqual(animated["data-final-value"], "$35M")

    def test_stat_has_no_description_field(self):
        self.assertEqual(list(ImpactStatBlock().child_blocks), ["stat_number", "stat_heading"])

    def test_ignores_description_left_in_saved_data(self):
        stats = [{**stat, "stat_description": "legacy copy"} for stat in STATS]

        soup = self.render(stats)

        self.assertNotIn("legacy copy", soup.get_text())
        self.assertEqual(len(soup.select(".mzf-c-card--statistic")), 3)

    def test_renders_without_the_foundation_grid_wrapper(self):
        self.assertTrue(ImpactNumberBlock().skip_default_wrapper)
