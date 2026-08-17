from django.test import TestCase
from wagtail.blocks import StructBlockValidationError

from foundation_cms.blocks.factories import CustomMediaBlockFactory
from foundation_cms.blocks.media_block import CustomMediaBlock
from foundation_cms.blocks.tests.helpers import build_clean_image
from foundation_cms.validators import VIMEO_MP4_URL_HELP_TEXT


class TestCustomMediaBlockClean(TestCase):
    def test_valid_image_content(self):
        """Image content type with an image set should pass validation."""
        block = CustomMediaBlockFactory(content="image", image=build_clean_image())
        CustomMediaBlock().clean(block)

    def test_invalid_image_content_missing_image(self):
        """Image content type with no image set should fail validation."""
        block = CustomMediaBlockFactory(content="image", image=None)

        with self.assertRaises(StructBlockValidationError) as cm:
            CustomMediaBlock().clean(block)

        self.assertEqual(
            cm.exception.block_errors["image"].message,
            "Image was chosen as content type, but no image is set.",
        )

    def test_valid_video_content(self):
        """Video content type with a valid Vimeo mp4 URL should pass validation."""
        block = CustomMediaBlockFactory(
            content="video",
            video_url=("https://player.vimeo.com/progressive_redirect/playback/123456789/rendition/1080p/file.mp4"),
        )
        CustomMediaBlock().clean(block)

    def test_invalid_video_content_missing_url(self):
        """Video content type with no URL set should fail validation."""
        block = CustomMediaBlockFactory(content="video", video_url="")

        with self.assertRaises(StructBlockValidationError) as cm:
            CustomMediaBlock().clean(block)

        self.assertEqual(
            cm.exception.block_errors["video_url"].message,
            "Video was chosen as content type, but no URL is set.",
        )

    def test_invalid_video_content_bad_url_format(self):
        """Video content type with a non-mp4 Vimeo URL should fail validation."""
        block = CustomMediaBlockFactory(content="video", video_url="https://vimeo.com/123456789")

        with self.assertRaises(StructBlockValidationError) as cm:
            CustomMediaBlock().clean(block)

        self.assertEqual(cm.exception.block_errors["video_url"].message, VIMEO_MP4_URL_HELP_TEXT)
