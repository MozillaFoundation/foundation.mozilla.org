from django.test import TestCase
from wagtail.blocks import StructBlockValidationError

from foundation_cms.blocks.factories import VideoBlockFactory
from foundation_cms.blocks.video_block import VideoBlock
from foundation_cms.validators import VIMEO_HELP_TEXT


class TestVideoBlockClean(TestCase):
    def test_valid_video_url(self):
        """A valid Vimeo URL should pass validation."""
        block = VideoBlockFactory(video_url="https://vimeo.com/123456789")
        VideoBlock().clean(block)

    def test_invalid_missing_video_url(self):
        """An empty video URL should fail validation."""
        block = VideoBlockFactory(video_url="")

        with self.assertRaises(StructBlockValidationError) as cm:
            VideoBlock().clean(block)

        self.assertEqual(cm.exception.block_errors["video_url"].message, VIMEO_HELP_TEXT)

    def test_invalid_bad_video_url_format(self):
        """A non-Vimeo URL should fail validation."""
        block = VideoBlockFactory(video_url="not-a-url")

        with self.assertRaises(StructBlockValidationError) as cm:
            VideoBlock().clean(block)

        self.assertEqual(cm.exception.block_errors["video_url"].message, VIMEO_HELP_TEXT)
