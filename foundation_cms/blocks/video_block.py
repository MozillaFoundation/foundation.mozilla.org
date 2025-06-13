import re
from django.core.exceptions import ValidationError
from wagtail import blocks
from foundation_cms.base.models.base_block import BaseBlock
from foundation_cms.blocks.link_block import LinkWithoutLabelBlock

class VideoBlock(BaseBlock):

    video_url = blocks.URLBlock(
        required=True,
        label="Video Embed URL",
    )
    caption = blocks.CharBlock(
        required=False,
        label="Caption Text"
    )
    caption_url = LinkWithoutLabelBlock(
        required=False,
        help_text="Optional URL the caption should link to."
    )


    class Meta:
        template_name = "video_block.html"
        icon = "media"
        label = "Video Block"
