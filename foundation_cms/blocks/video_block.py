from wagtail import blocks

from foundation_cms.base.models.base_block import BaseBlock
from foundation_cms.blocks.link_block import LinkWithoutLabelBlock


class VideoBlock(BaseBlock):
    video_id = blocks.CharBlock(
        required=True,
        label="Vimeo Video ID",
        help_text=("Log into Vimeo, select your desired video, and copy its ID. (Found in the URL)"),
    )
    caption = blocks.CharBlock(required=False, help_text="Optional Caption Text")
    caption_url = blocks.ListBlock(
        LinkWithoutLabelBlock(),
        min_num=0,
        max_num=1,
        help_text="Optional URL that this caption should link out to.",
    )

    class Meta:
        template_name = "video_block.html"
        icon = "media"
        label = "Video Block"
