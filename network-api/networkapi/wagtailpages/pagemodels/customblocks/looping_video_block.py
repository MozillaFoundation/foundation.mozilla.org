from wagtail.core import blocks


class LoopingVideoBlock(blocks.StructBlock):
    video_url = blocks.CharBlock(
        help_text='Visit your desired video on Vimeo, '
                  'then click "Advanced", "Distribution", '
                  'and "Video File Links". Copy and paste the link here.'
    )

    class Meta:
        template = 'wagtailpages/blocks/looping_video_block.html'
