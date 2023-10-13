from django.core.exceptions import ValidationError
from django.test import TestCase
from wagtail import rich_text
from wagtail.images.tests.utils import Image, get_test_image_file

from networkapi.donate.pagemodels.customblocks.notice_block import NoticeBlock


class NoticeBlockTest(TestCase):
    def setUp(self):
        self.notice_block = NoticeBlock()

    def test_valid_notice_block(self):
        value = {
            "image": Image.objects.create(title="Test Image", file=get_test_image_file()),
            "image_alt_text": "Alt text",
            "text": rich_text.RichText("<p>Some content</p>"),
        }
        # If clean method does not raise ValidationError, the test will pass
        self.notice_block.clean(value)

    def test_image_without_alt_text_raises_error(self):
        value = {
            "image": Image.objects.create(title="Test Image", file=get_test_image_file()),
            "image_alt_text": "",
            "text": rich_text.RichText("<p>Some content</p>"),
        }
        with self.assertRaisesMessage(ValidationError, "Image must include alt text."):
            self.notice_block.clean(value)

    def test_alt_text_without_image_raises_error(self):
        value = {
            "image": None,
            "image_alt_text": "Alt text",
            "text": rich_text.RichText("<p>Some content</p>"),
        }
        with self.assertRaisesMessage(ValidationError, "Alt text must have an associated image."):
            self.notice_block.clean(value)

    def test_valid_block_without_image_and_alt_text(self):
        value = {
            "image": None,
            "image_alt_text": "",
            "text": rich_text.RichText("<p>Some content</p>"),
        }
        # If clean method does not raise ValidationError, the test will pass
        self.notice_block.clean(value)
