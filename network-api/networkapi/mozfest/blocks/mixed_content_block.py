from django.forms.utils import ErrorList
from wagtail import blocks
from wagtail.blocks import struct_block
from wagtail.images import blocks as image_blocks

from networkapi.wagtailpages.pagemodels.customblocks import listing as listing_blocks


class VideoBlock(blocks.StructBlock):
    url = blocks.CharBlock(
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
        help_text="Text content to display withe video title.",
    )
    thumbnail = image_blocks.ImageChooserBlock(help_text="The image to show before the video is played.")

    class Meta:
        icon = "media"


class MixedContentBlock(blocks.StructBlock):
    video = VideoBlock(max_num=1)
    cards = blocks.ListBlock(listing_blocks.ListingCard(), min_num=1, max_num=4)
    link_url = blocks.URLBlock(required=False)
    link_text = blocks.CharBlock(required=False, max_length=50)

    def clean(self, value):
        result = super().clean(value)

        link_url = value.get("link_url")
        link_text = value.get("link_text")

        if link_url and not link_text:
            raise struct_block.StructBlockValidationError(
                {"link_text": ErrorList(["Please add a text value for the link."])}
            )

        if link_text and not link_url:
            raise struct_block.StructBlockValidationError(
                {"link_url": ErrorList(["Please add a URL value for the link."])}
            )

        return result

    class Meta:
        template = "fragments/blocks/mixed_content_block.html"
