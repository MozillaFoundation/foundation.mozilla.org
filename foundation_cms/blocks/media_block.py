from django import forms
from django.core.exceptions import ValidationError
from django.utils.functional import cached_property
from wagtail.blocks import CharBlock, ChoiceBlock, StructBlockValidationError
from wagtail.blocks.struct_block import StructBlockAdapter
from wagtail.images.blocks import ImageBlock
from wagtail.telepath import register

from foundation_cms.base.models.base_block import BaseBlock
from foundation_cms.validators import validate_vimeo_mp4_url


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
        form_template = "patterns/admin/media_block_form.html"
        form_attrs = {
            "data-controller": "media",
            "data-media-trigger-field-value": "content",
        }

    # Custom validation to ensure required fields are set based on content type
    def clean(self, value):
        cleaned_data = super().clean(value)
        validation_errors = {}

        # Image-specific validation
        if cleaned_data["content"] == "image" and not cleaned_data.get("image"):
            validation_errors["image"] = ValidationError("Image was chosen as content type, but no image is set.")

        # Video-specific validation, including Vimeo MP4 URL format
        if cleaned_data["content"] == "video":
            video_url = cleaned_data.get("video_url")
            if not video_url:
                validation_errors["video_url"] = ValidationError(
                    "Video was chosen as content type, but no URL is set."
                )
            else:
                try:
                    validate_vimeo_mp4_url(video_url)
                except ValidationError as e:
                    validation_errors["video_url"] = ValidationError(e)

        if validation_errors:
            raise StructBlockValidationError(validation_errors)

        return cleaned_data


class CustomMediaBlockAdapter(StructBlockAdapter):
    @cached_property
    def media(self):
        structblock_media = super().media
        return forms.Media(js=structblock_media._js + ["foundation_cms/_js/admin_controllers.compiled.js"])


register(CustomMediaBlockAdapter(), CustomMediaBlock)
