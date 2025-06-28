from django.core.exceptions import ValidationError
from wagtail import blocks
from wagtail.blocks import StructBlockValidationError

from foundation_cms.base.models.base_block import BaseBlock
from foundation_cms.blocks.link_block import LinkWithoutLabelBlock
from foundation_cms.validators import validate_vimeo_url


class VideoBlock(BaseBlock):
    video_url = blocks.CharBlock(
        required=True,
        label="Vimeo Video URL",
        help_text=("Log into Vimeo, select your desired video, and click 'Copy Link'"),
    )
    caption = blocks.CharBlock(required=False, help_text="Optional Caption Text")
    caption_url = blocks.ListBlock(
        LinkWithoutLabelBlock(),
        min_num=0,
        max_num=1,
        help_text="Optional URL that this caption should link out to.",
        default=[],
    )

    def clean(self, value):
        validation_errors = {}

        # Run custom Vimeo URL validation
        try:
            validate_vimeo_url(value.get("video_url", ""))
        except ValidationError as e:
            validation_errors["video_url"] = ValidationError(e)

        if validation_errors:
            raise StructBlockValidationError(validation_errors)

        return super().clean(value)

    class Meta:
        template_name = "video_block.html"
        icon = "media"
        label = "Video Block"
