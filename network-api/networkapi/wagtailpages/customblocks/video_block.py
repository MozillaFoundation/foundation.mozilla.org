from wagtail.core import blocks


class VideoBlock(blocks.StructBlock):
    url = blocks.CharBlock(
        help_text='Please make sure this is a proper embed URL, or your video will not show up on the page.'
    )
    caption = blocks.CharBlock(
        required=False,
    )
    captionURL = blocks.CharBlock(
        required=False,
        help_text='Optional URL for caption to link to.'
    )

    class Meta:
        template = 'wagtailpages/blocks/video_block.html'
