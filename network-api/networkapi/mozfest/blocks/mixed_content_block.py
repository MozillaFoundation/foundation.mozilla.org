from wagtail import blocks
from wagtail.images import blocks as image_blocks

from networkapi.wagtailpages.pagemodels.customblocks import listing as listing_blocks
from networkapi.wagtailpages.pagemodels.customblocks.link_block import LinkBlock


class VideoBlock(blocks.StructBlock):
    url = blocks.URLBlock(
        label="Embed URL",
        help_text="For YouTube: go to your YouTube video and click “Share,” "
        "then “Embed,” and then copy and paste the provided URL only. "
        "For example: https://www.youtube.com/embed/3FIVXBawyQw "
        "For Vimeo: follow similar steps to grab the embed URL. "
        "For example: https://player.vimeo.com/video/9004979",
    )
    caption = blocks.CharBlock(
        required=False,
        max_length=25,
        help_text="Optional caption for the video, displayed next to the play button.",
    )
    title = blocks.CharBlock(
        required=False,
        max_length=50,
        help_text="Optional title for the video.",
    )
    text = blocks.CharBlock(
        required=False,
        help_text="Text content to display with the video title.",
    )
    thumbnail = image_blocks.ImageChooserBlock(help_text="The image to show before the video is played.")

    class Meta:
        icon = "media"
        template = "fragments/blocks/video_block.html"


class MixedContentBlock(blocks.StructBlock):
    video = VideoBlock()
    cards = blocks.ListBlock(listing_blocks.ListingCard(), min_num=1, max_num=4)
    link = blocks.ListBlock(
        LinkBlock(),
        min_num=0,
        max_num=1,
        help_text="Optional link that this mixed content block should link out to.",
    )

    class Meta:
        template = "fragments/blocks/mixed_content_block.html"
