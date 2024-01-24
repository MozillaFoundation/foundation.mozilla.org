from django.test import TestCase
from wagtail import rich_text
from wagtail.blocks.struct_block import StructBlockValidationError
from wagtail.images.tests.utils import Image, get_test_image_file

from networkapi.donate.factory.customblocks.notice_block import NoticeBlockFactory
from networkapi.donate.pagemodels.customblocks.notice_block import NoticeBlock


class NoticeBlockTest(TestCase):
    def setUp(self):
        self.notice_block = NoticeBlock()

    def test_notice_block_factory(self):
        """
        Testing that the factory can successfully create a valid NoticeBlock.
        """
        notice_block_factory_default_values = NoticeBlockFactory()

        is_valid = self.notice_block.clean(notice_block_factory_default_values)

        self.assertTrue(is_valid)

    def test_valid_notice_block(self):
        """
        Testing that a notice block with all fields is valid.
        """
        value = {
            "image": Image.objects.create(title="Test Image", file=get_test_image_file()),
            "image_alt_text": "Alt text",
            "text": rich_text.RichText("<p>Some content</p>"),
        }

        is_valid = self.notice_block.clean(value)

        self.assertTrue(is_valid)

    def test_image_without_alt_text_raises_error(self):
        """
        Testing that a notice block with an image but no alt text is invalid.
        """
        value = {
            "image": Image.objects.create(title="Test Image", file=get_test_image_file()),
            "image_alt_text": "",
            "text": rich_text.RichText("<p>Some content</p>"),
        }

        with self.assertRaises(StructBlockValidationError) as catcher:
            self.notice_block.clean(value)
        exceptions = catcher.exception.as_json_data()["blockErrors"]
        self.assertCountEqual(exceptions["image"]["messages"], ["Image must include alt text."])

    def test_alt_text_without_image_raises_error(self):
        """
        Testing that a notice block with alt text but no image is invalid.
        """
        value = {
            "image": None,
            "image_alt_text": "Alt text",
            "text": rich_text.RichText("<p>Some content</p>"),
        }

        with self.assertRaises(StructBlockValidationError) as catcher:
            self.notice_block.clean(value)
        exceptions = catcher.exception.as_json_data()["blockErrors"]
        self.assertCountEqual(exceptions["image_alt_text"]["messages"], ["Alt text must have an associated image."])

    def test_notice_text_field_is_required(self):
        """
        Testing that a notice block with no body text is invalid.
        """
        value = {
            "image": Image.objects.create(title="Test Image", file=get_test_image_file()),
            "image_alt_text": "Alt text",
            "text": rich_text.RichText(""),
        }

        with self.assertRaises(StructBlockValidationError) as catcher:
            self.notice_block.clean(value)
        exceptions = catcher.exception.as_json_data()["blockErrors"]
        self.assertCountEqual(exceptions["text"]["messages"], ["This field is required."])

    def test_valid_block_without_image_and_alt_text(self):
        """
        Testing that a notice block with only text is valid.
        """
        value = {
            "image": None,
            "image_alt_text": "",
            "text": rich_text.RichText("<p>Some content</p>"),
        }

        is_valid = self.notice_block.clean(value)

        self.assertTrue(is_valid)
