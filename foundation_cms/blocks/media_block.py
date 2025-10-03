from django import forms
from django.core.exceptions import ValidationError
from django.utils.functional import cached_property
from wagtail.telepath import register
from wagtail.blocks import CharBlock, ChoiceBlock
from wagtail.blocks.struct_block import StructBlockAdapter
from wagtail.images.blocks import ImageBlock

from foundation_cms.base.models.base_block import BaseBlock


class CustomMediaBlock(BaseBlock):
    """
    A reusable media block with title and orientation options
    """

    title = CharBlock(required=False, help_text="Title/caption for this media")

    content = ChoiceBlock(
        choices=[
            ("image", "Image"),
            ("video", "Video"),
        ],
        default="image",
        help_text="Select the type of media to display",
    )

    image = ImageBlock(required=False)

    video_url = CharBlock(
        required=False,
        max_length=500,
        help_text="Log into Vimeo using 1Password "
        "and upload the desired video. "
        "Then select the video and "
        'click "...", "Video File Links", '
        'and select "(mp4, 1920 x 1080)". Copy and paste the link here.',
    )

    orientation = ChoiceBlock(
        choices=[
            ("portrait", "Portrait"),
            ("landscape", "Landscape"),
            ("square", "Square"),
        ],
        default="landscape",
        help_text="Select the orientation of this media",
    )

    class Meta:
        icon = "image"
        template_name = "media_block.html"
        label = "Media"
        form_template = "patterns/blocks/themes/default/media_block_form.html"
        form_attrs = {
            "data-controller": "media",
            "data-media-trigger-field-value": "content",
        }

    # Custom validation to ensure required fields are set based on content type
    def clean(self, value):
        cleaned_data = super().clean(value)
        errors = {}

        if cleaned_data["content"] == "image" and not cleaned_data.get("image"):
            errors["image"] = "Image was chosen as content type, but no image is set."

        if cleaned_data["content"] == "video" and not cleaned_data.get("video_url"):
            errors["video_url"] = "Video was chosen as content type, but no URL is set."

        if errors:
            raise ValidationError(errors)

        return cleaned_data


class CustomMediaBlockAdapter(StructBlockAdapter):
    @cached_property
    def media(self):
        structblock_media = super().media
        return forms.Media(
            js=structblock_media._js + ["foundation_cms/_js/admin_controllers.compiled.js"]
        )


register(CustomMediaBlockAdapter(), CustomMediaBlock)
