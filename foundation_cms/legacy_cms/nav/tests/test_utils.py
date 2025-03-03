import json
from pathlib import Path
from unittest import TestCase

from foundation_cms.legacy_cms.nav import utils


class TestUtils(TestCase):
    def test_nested_key_not_found(self):
        d = {"a": {"b": {"c": {"d": 1}}}}
        result = list(utils.find_key_values(d, "key"))
        self.assertEqual(result, [])

    def test_multiple_key_value_pairs(self):
        d = {"a": [1, 2, 3], "b": {"a": 4, "b": 5}, "c": [{"a": 6}, {"a": 7}]}
        result = list(utils.find_key_values(d, "a"))
        print(result)
        self.assertEqual(result, [[1, 2, 3], 4, 6, 7])

    def test_non_string_keys(self):
        d = {1: "a", 2: "b", 3: "c"}
        result = list(utils.find_key_values(d, 1))
        self.assertEqual(result, ["a"])

    def test_non_hashable_values(self):
        d = {"a": [1, 2, 3], "b": {"c": [4, 5, 6]}, "d": 7}
        result = list(utils.find_key_values(d, "c"))
        expected = [[4, 5, 6]]
        self.assertEqual(result, expected)

    def test_extract_values_from_nested_dictionaries(self):
        d = {"id": 4, "a": {"id": 3, "b": {"id": 2, "c": {"id": 1}}}}
        result = list(utils.find_key_values(d, "id"))
        self.assertEqual(result, [4, 3, 2, 1])

    def test_dropdown_data(self):
        """Tests that the function can extract the page values from a menu dropdowns field's raw data."""
        current_dir = Path(__file__).parent
        json_file = current_dir / "fixtures/dropdown_data.json"
        with open(json_file) as f:
            d = json.load(f)
        pages = []
        for dictionary in d:
            local_result = list(utils.find_key_values(dictionary, "page"))
            pages.extend(local_result)
        pages = [page for page in pages if page]
        expected = [587, 586, 588]
        self.assertEqual(pages, expected)
