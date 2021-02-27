from wagtail.core import blocks


class VideoBlock(blocks.StructBlock):
    url = blocks.CharBlock(
        help_text='For YouTube: go to your YouTube video and click “Share,” '
                  'then “Embed,” and then copy and paste the provided URL only. '
                  'For example: https://www.youtube.com/embed/3FIVXBawyQw '
                  'For Vimeo: follow similar steps to grab the embed URL. '
                  'For example: https://player.vimeo.com/video/9004979'
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
