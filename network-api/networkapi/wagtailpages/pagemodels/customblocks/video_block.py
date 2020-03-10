from wagtail.core import blocks


class VideoBlock(blocks.StructBlock):
    url = blocks.CharBlock(
        help_text='To make sure a video will embed properly, go to your YouTube video and click “Share,” '
                  'then “Embed,” and then copy and paste the provided URL only. '
                  'For example: https://www.youtube.com/embed/3FIVXBawyQw'
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
