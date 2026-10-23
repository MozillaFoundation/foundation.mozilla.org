from django.test import TestCase
from wagtail.blocks import StructBlockValidationError

from foundation_cms.blocks.factories import VideoBlockFactory
from foundation_cms.blocks.video_block import VideoBlock
from foundation_cms.validators import (
    VIMEO_VIDEO_OR_EVENT_HELP_TEXT,
    get_vimeo_embed_url,
)


class TestVideoBlockClean(TestCase):
    def test_valid_video_url(self):
        """A valid Vimeo URL should pass validation."""
        block = VideoBlockFactory(video_url="https://vimeo.com/123456789")
        VideoBlock().clean(block)

    def test_valid_event_url(self):
        """A Vimeo event URL should pass validation."""
        block = VideoBlockFactory(video_url="https://vimeo.com/event/6295860")
        VideoBlock().clean(block)

    def test_invalid_missing_video_url(self):
        """An empty video URL should fail validation."""
        block = VideoBlockFactory(video_url="")

        with self.assertRaises(StructBlockValidationError) as cm:
            VideoBlock().clean(block)

        self.assertEqual(cm.exception.block_errors["video_url"].message, VIMEO_VIDEO_OR_EVENT_HELP_TEXT)

    def test_invalid_bad_video_url_format(self):
        """A non-Vimeo URL should fail validation."""
        block = VideoBlockFactory(video_url="not-a-url")

        with self.assertRaises(StructBlockValidationError) as cm:
            VideoBlock().clean(block)

        self.assertEqual(cm.exception.block_errors["video_url"].message, VIMEO_VIDEO_OR_EVENT_HELP_TEXT)


class TestVideoBlockEmbedUrl(TestCase):
    def test_video_urls(self):
        for url in [
            "https://vimeo.com/123456789",
            "https://www.vimeo.com/123456789",
            "https://player.vimeo.com/video/123456789",
        ]:
            with self.subTest(url=url):
                self.assertEqual(get_vimeo_embed_url(url), "https://player.vimeo.com/video/123456789")

    def test_event_url(self):
        self.assertEqual(
            get_vimeo_embed_url("https://vimeo.com/event/6295860"),
            "https://vimeo.com/event/6295860/embed",
        )

    def test_unlisted_video_keeps_privacy_hash(self):
        for url in [
            "https://vimeo.com/123456789?h=5e2d1c1e6d",
            "https://player.vimeo.com/video/123456789?h=5e2d1c1e6d",
        ]:
            with self.subTest(url=url):
                self.assertEqual(get_vimeo_embed_url(url), "https://player.vimeo.com/video/123456789?h=5e2d1c1e6d")

    def test_video_keeps_playback_options_and_start_time(self):
        self.assertEqual(
            get_vimeo_embed_url("https://vimeo.com/123456789?autoplay=1&muted=1#t=30s"),
            "https://player.vimeo.com/video/123456789?autoplay=1&muted=1#t=30s",
        )

    def test_render_uses_embed_url(self):
        block = VideoBlock()
        value = block.to_python({"video_url": "https://vimeo.com/event/6295860"})
        self.assertIn('src="https://vimeo.com/event/6295860/embed"', block.render(value))

    def test_render_without_url_omits_iframe(self):
        block = VideoBlock()
        for data in [{}, {"video_url": "https://vimeo.com/channels/staffpicks/123"}]:
            with self.subTest(data=data):
                self.assertNotIn("video-block__wrapper", block.render(block.to_python(data)))
