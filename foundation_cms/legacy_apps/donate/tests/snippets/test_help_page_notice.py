from django.core.exceptions import ValidationError
from django.test import TestCase

from foundation_cms.legacy_apps.donate.factory.snippets.help_page_notice import (
    HelpPageNoticeFactory,
)
from foundation_cms.legacy_apps.donate.snippets.help_page_notice import HelpPageNotice
from foundation_cms.legacy_apps.wagtailpages.factory.image_factory import ImageFactory


class HelpPageNoticeTest(TestCase):
    def setUp(self):
        self.notice = HelpPageNotice()

    def test_help_page_notice_factory(self):
        """
        Testing that the factory can successfully create a valid HelpPageNotice.
        """
        HelpPageNoticeFactory()

    def test_valid_help_page_notice(self):
        """
        Testing that a HelpPageNotice with all fields is valid.
        """
        notice = HelpPageNotice(
            name="Test Notice",
            text="<p>Some content</p>",
            notice_image=ImageFactory(),
            notice_image_alt_text="Alt text",
        )

        # Clean should not raise any validation error
        notice.full_clean()

    def test_image_without_alt_text_raises_error(self):
        """
        Testing that a HelpPageNotice with an image but no alt text is invalid.
        """
        notice = HelpPageNotice(
            name="Test Notice", text="<p>Some content</p>", notice_image=ImageFactory(), notice_image_alt_text=""
        )

        with self.assertRaises(ValidationError) as context:
            notice.full_clean()
        self.assertIn("Image must include alt text.", str(context.exception))

    def test_alt_text_without_image_raises_error(self):
        """
        Testing that a HelpPageNotice with alt text but no image is invalid.
        """
        notice = HelpPageNotice(
            name="Test Notice", text="<p>Some content</p>", notice_image=None, notice_image_alt_text="Alt text"
        )

        with self.assertRaises(ValidationError) as context:
            notice.full_clean()
        self.assertIn("Alt text must have an associated image.", str(context.exception))

    def test_valid_notice_without_image_and_alt_text(self):
        """
        Testing that a HelpPageNotice with only text is valid.
        """
        notice = HelpPageNotice(
            name="Test Notice", text="<p>Some content</p>", notice_image=None, notice_image_alt_text=""
        )

        # Clean should not raise any validation error
        notice.full_clean()

    def test_notice_text_field_is_required(self):
        """
        Testing that a HelpPageNotice with no body text is invalid.
        """
        notice = HelpPageNotice(
            name="Test Notice", text="", notice_image=ImageFactory(), notice_image_alt_text="Alt text"
        )

        with self.assertRaises(ValidationError) as context:
            notice.full_clean()
        self.assertIn("This field cannot be blank.", str(context.exception))
