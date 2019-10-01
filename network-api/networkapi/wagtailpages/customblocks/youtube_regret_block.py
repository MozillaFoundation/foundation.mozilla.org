from wagtail.core import blocks


class YoutubeRegretBlock(blocks.StructBlock):
    heading = blocks.CharBlock(
        help_text='Temporary youtube regret block.'
    )

    class Meta:
        template = 'wagtailpages/blocks/youtube_regret_block.html'
