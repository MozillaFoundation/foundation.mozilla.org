from django.core.exceptions import ValidationError
from django.db import models

from foundation_cms.mixins.hero_image import HeroImageMixin


class HeroMediaMixin(HeroImageMixin):
    """Extends HeroImageMixin to add video support and media type selection."""

    HERO_CONTENT_IMAGE = "image"
    HERO_CONTENT_VIDEO = "video"

    displayed_hero_content = models.CharField(
        verbose_name="Select media type from dropdown",
        max_length=25,
        choices=[
            (HERO_CONTENT_IMAGE, "Image"),
            (HERO_CONTENT_VIDEO, "Video"),
        ],
        default=HERO_CONTENT_IMAGE,
    )

    hero_video_url = models.CharField(
        blank=True,
        max_length=500,
        help_text="Log into Vimeo using 1Password and upload the desired video. "
        "Then select the video and click '...', 'Video File Links', "
        "and select '(mp4, 1920 x 1080)'. Copy and paste the link here.",
    )

    class Meta:
        abstract = True

    def clean(self):
        super().clean()
        errors = {}

        if self.displayed_hero_content == self.HERO_CONTENT_IMAGE and not self.hero_image:
            errors["hero_image"] = "Image was chosen as displayed hero content, but no image is set."

        if self.displayed_hero_content == self.HERO_CONTENT_VIDEO and not self.hero_video_url:
            errors["hero_video_url"] = "Video was chosen as displayed hero content, but no URL is set."

        if errors:
            raise ValidationError(errors)
