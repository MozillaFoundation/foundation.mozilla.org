import re
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from django.core.exceptions import ValidationError


class VideoPanelBlock(blocks.StructBlock):
    VIMEO_HELP_TEXT = (
        "Please enter a valid Vimeo URL (e.g. https://vimeo.com/123456789 or https://player.vimeo.com/video/123456789)."
    )

    label = blocks.CharBlock(required=True)
    heading = blocks.CharBlock(required=False)
    thumbnail = ImageChooserBlock(required=True)
    video_url = blocks.URLBlock(required=True, help_text=VIMEO_HELP_TEXT)

    def clean(self, value):
        cleaned = super().clean(value)
        url = cleaned.get("video_url", "")

        # Allow regular and embed Vimeo formats
        vimeo_pattern = r"^https?://(www\.)?(vimeo\.com|player\.vimeo\.com/video)/\d+"

        if not re.match(vimeo_pattern, url):
            raise ValidationError({
                "video_url": self.VIMEO_HELP_TEXT
            })

        return cleaned


    class Meta:
        icon = "media"
        label = "Video Panel"


class ImageTextPanelBlock(blocks.StructBlock):
    label = blocks.CharBlock(required=True)
    heading = blocks.CharBlock(required=True)
    image = ImageChooserBlock(required=True)
    cta_text = blocks.CharBlock(required=True)
    cta_link = blocks.URLBlock(required=True)
    description = blocks.TextBlock(required=False)

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
