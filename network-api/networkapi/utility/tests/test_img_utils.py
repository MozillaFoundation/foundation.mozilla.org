import tempfile
from unittest import mock

from django.test import TestCase

from networkapi.utility.templatetags import img_utils


@mock.patch("networkapi.utility.templatetags.img_utils.find")
class IncludeSVGTests(TestCase):
    def setUp(self):
        self.valid_svg = (
            '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="none" stroke="#CCC">'
            '<path stroke-linecap="round" stroke-linejoin="round" '
            'stroke-width="1.5" d="m5.25 12.75 7.5-7.5M5.25 5.25h7.5v7.5"/>'
            "</svg>"
        )
        self.temp_svg = tempfile.NamedTemporaryFile(suffix=".svg", delete=False)
        self.temp_svg.write(str.encode(self.valid_svg))
        self.temp_svg.close()

    def test_valid_path(self, mock_find):
        path = "path/to/valid.svg"
        mock_find.return_value = self.temp_svg.name
        result = img_utils.include_svg(path)
        self.assertEqual(result, self.valid_svg)

    def test_svg_not_found(self, mock_find):
        path = "path/to/nonexistent.svg"
        mock_find.return_value = None
        with self.assertRaises(ValueError):
            img_utils.include_svg(path)

    def test_path_to_non_svg(self, mock_find):
        path = "path/to/invalid.png"
        with self.assertRaises(ValueError):
            img_utils.include_svg(path)
