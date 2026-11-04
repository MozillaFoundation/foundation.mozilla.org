from django.core.exceptions import ValidationError
from wagtail import blocks
from wagtail.blocks import StructBlockValidationError

from foundation_cms.base.models.base_block import BaseBlock
from foundation_cms.blocks.link_block import LinkWithoutLabelBlock
from foundation_cms.validators import (
    get_vimeo_embed_url,
    validate_vimeo_video_or_event_url,
)


class VideoBlock(BaseBlock):
    video_url = blocks.CharBlock(
        required=True,
        label="Vimeo Video or Event URL",
        help_text=("Log into Vimeo, select your desired video or event, and click 'Copy Link'"),
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
            validate_vimeo_video_or_event_url(value.get("video_url", ""))
        except ValidationError as e:
            validation_errors["video_url"] = ValidationError(e)

        if validation_errors:
            raise StructBlockValidationError(validation_errors)

        return super().clean(value)

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context["embed_url"] = get_vimeo_embed_url(value["video_url"] or "")
        return context

    class Meta:
        template_name = "video_block.html"
        icon = "media"
        label = "Video Block"
