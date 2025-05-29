import re

from django.core.exceptions import ValidationError
from wagtail import blocks
from wagtail.images.blocks import ImageBlock


class VideoPanelBlock(blocks.StructBlock):
    VIMEO_HELP_TEXT = "Please enter a valid Vimeo URL (e.g. https://vimeo.com/123456789 or https://player.vimeo.com/video/123456789)."

    label = blocks.CharBlock(required=True)
    heading = blocks.CharBlock(required=False, max_length=40)
    thumbnail = ImageBlock(required=True)
    video_url = blocks.URLBlock(required=True, help_text=VIMEO_HELP_TEXT)

    def clean(self, value):
        cleaned = super().clean(value)
        url = cleaned.get("video_url", "")
        errors = {}

        # Allow regular and embed Vimeo formats
        vimeo_pattern = r"^https?://(www\.)?(vimeo\.com|player\.vimeo\.com/video)/\d+"

        if not re.match(vimeo_pattern, url):
            errors["video_url"] = self.VIMEO_HELP_TEXT

        if errors:
            raise ValidationError(errors)

        return cleaned

    class Meta:
        icon = "media"
        label = "Video Panel"


class ImageTextPanelBlock(blocks.StructBlock):
    label = blocks.CharBlock(required=True)
    heading = blocks.CharBlock(required=True, max_length=40)
    image = ImageBlock(required=True)
    cta_text = blocks.CharBlock(required=True)
    cta_link = blocks.URLBlock(required=True)
    description = blocks.TextBlock(required=False, max_length=100)

    def clean(self, value):
        cleaned = super().clean(value)
        cta_text = cleaned.get("cta_text", "")
        errors = {}

        if len(cta_text.split()) > 4:
            errors["cta_text"] = "CTA text must be fewer than 4 words."

        if errors:
            raise ValidationError(errors)

        return cleaned

    class Meta:
        icon = "image"
        label = "Image + Text Panel"


class HeroAccordionBlock(blocks.StreamBlock):
    def __init__(self, min_panels=2, max_panels=3, max_video_panels=1, **kwargs):
        self.min_panels = min_panels
        self.max_panels = max_panels
        self.max_video_panels = max_video_panels
        super().__init__(**kwargs)

    video_panel = VideoPanelBlock()
    image_text_panel = ImageTextPanelBlock()

    def clean(self, value):
        cleaned = super().clean(value)
        video_count = sum(1 for block in cleaned if block.block_type == "video_panel")

        if len(cleaned) < self.min_panels:
            raise ValidationError(f"There must be at least {self.min_panels} panels.")
        if len(cleaned) > self.max_panels:
            raise ValidationError(f"There can be at most {self.max_panels} panels.")
        if video_count > self.max_video_panels:
            raise ValidationError(f"Only {self.max_video_panels} video panel(s) allowed.")

        return cleaned
