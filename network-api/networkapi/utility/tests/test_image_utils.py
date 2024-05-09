from django.core.exceptions import ValidationError
from django.test import TestCase

from networkapi.utility.images import SVGImageFormatValidator
from networkapi.wagtailpages.factory.image_factory import ImageFactory


class SVGImageFormatValidatorTests(TestCase):

    def test_svg_image_format_validator_accepts_svg(self):
        # Create an SVG image using the ImageFactory
        svg_image = ImageFactory(file__filename="icon.svg", file__extension="svg")
        # No exception should be raised for SVG files
        try:
            SVGImageFormatValidator(svg_image)
        except ValidationError:
            self.fail("SVGImageFormatValidator unexpectedly raised ValidationError for an SVG file.")

    def test_svg_image_format_validator_rejects_non_svg(self):
        # List of non-SVG file types to test
        non_svg_files = [
            ("icon.jpg", "jpg"),
            ("icon.png", "png"),
            ("icon.gif", "gif"),
            ("icon.pdf", "pdf"),
        ]

        # Loop through the file list and check that validation fails
        for filename, extension in non_svg_files:
            with self.subTest(filename=filename):
                non_svg_image = ImageFactory(file__filename=filename, file__extension=extension)
                with self.assertRaises(ValidationError):
                    SVGImageFormatValidator(non_svg_image)
