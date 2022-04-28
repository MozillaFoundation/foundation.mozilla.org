from wagtail.core import blocks


class LoopingVideoBlock(blocks.StructBlock):
    video_url = blocks.CharBlock(
        label='Embed URL',
        help_text='Log into Vimeo using 1Password '
                  'and upload the desired video. '
                  'Then select the video and '
                  'click "Advanced", "Distribution", '
                  'and "Video File Links". Copy and paste the link here.'
    )

    class Meta:
        template = 'wagtailpages/blocks/looping_video_block.html'
