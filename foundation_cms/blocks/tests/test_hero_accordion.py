from django.core.exceptions import ValidationError
from django.test import TestCase
from wagtail.blocks import StreamValue, StructBlockValidationError

from foundation_cms.blocks.factories import (
    ImageTextPanelBlockFactory,
    VideoPanelBlockFactory,
)
from foundation_cms.blocks.hero_accordion import (
    HeroAccordionBlock,
    ImageTextPanelBlock,
    VideoPanelBlock,
)
from foundation_cms.blocks.tests.helpers import build_clean_image
from foundation_cms.validators import VIMEO_HELP_TEXT


class TestVideoPanelBlockClean(TestCase):
    def test_valid_video_url(self):
        """A valid Vimeo URL should pass validation."""
        block = VideoPanelBlockFactory(thumbnail=build_clean_image(), video_url="https://vimeo.com/123456789")
        VideoPanelBlock().clean(block)

    def test_invalid_video_url(self):
        """An invalid video URL should fail validation."""
        block = VideoPanelBlockFactory(thumbnail=build_clean_image(), video_url="not-a-url")

        with self.assertRaises(StructBlockValidationError) as cm:
            VideoPanelBlock().clean(block)

        self.assertEqual(cm.exception.block_errors["video_url"].message, VIMEO_HELP_TEXT)


class TestImageTextPanelBlockClean(TestCase):
    def test_valid_cta_text(self):
        """A cta_text of 4 words or fewer (including empty) should pass validation."""
        block = ImageTextPanelBlockFactory(image=build_clean_image(), cta_text="one two three four")
        ImageTextPanelBlock().clean(block)

        block = ImageTextPanelBlockFactory(image=build_clean_image(), cta_text="")
        ImageTextPanelBlock().clean(block)

    def test_invalid_cta_text_too_many_words(self):
        """A cta_text of more than 4 words should fail validation."""
        block = ImageTextPanelBlockFactory(image=build_clean_image(), cta_text="one two three four five")

        # This clean() raises a plain ValidationError, not StructBlockValidationError.
        with self.assertRaises(ValidationError) as cm:
            ImageTextPanelBlock().clean(block)

        self.assertEqual(cm.exception.message_dict["cta_text"], ["CTA text must be fewer than 4 words."])


class TestHeroAccordionBlockClean(TestCase):
    def _make_stream(self, pairs):
        block_def = HeroAccordionBlock()
        return block_def, StreamValue(block_def, pairs)

    def test_valid_panel_count_and_video_count(self):
        """2-3 panels with at most 1 video panel should pass validation."""
        block_def, stream = self._make_stream(
            [
                (
                    "video_panel",
                    VideoPanelBlockFactory(thumbnail=build_clean_image(), video_url="https://vimeo.com/123456789"),
                ),
                ("image_text_panel", ImageTextPanelBlockFactory(image=build_clean_image())),
            ]
        )
        block_def.clean(stream)

    def test_invalid_too_few_panels(self):
        """Fewer than min_panels should fail validation."""
        block_def, stream = self._make_stream(
            [("image_text_panel", ImageTextPanelBlockFactory(image=build_clean_image()))]
        )

        with self.assertRaises(ValidationError) as cm:
            block_def.clean(stream)

        self.assertEqual(cm.exception.message, "There must be at least 2 panels.")

    def test_invalid_too_many_panels(self):
        """More than max_panels should fail validation."""
        block_def, stream = self._make_stream(
            [("image_text_panel", ImageTextPanelBlockFactory(image=build_clean_image())) for _ in range(4)]
        )

        with self.assertRaises(ValidationError) as cm:
            block_def.clean(stream)

        self.assertEqual(cm.exception.message, "There can be at most 3 panels.")

    def test_invalid_too_many_video_panels(self):
        """More than max_video_panels should fail validation."""
        block_def, stream = self._make_stream(
            [
                (
                    "video_panel",
                    VideoPanelBlockFactory(thumbnail=build_clean_image(), video_url="https://vimeo.com/111"),
                ),
                (
                    "video_panel",
                    VideoPanelBlockFactory(thumbnail=build_clean_image(), video_url="https://vimeo.com/222"),
                ),
            ]
        )

        with self.assertRaises(ValidationError) as cm:
            block_def.clean(stream)

        self.assertEqual(cm.exception.message, "Only 1 video panel allowed.")
