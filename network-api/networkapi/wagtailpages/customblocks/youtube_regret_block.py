from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class YoutubeRegretBlock(blocks.StructBlock):
    headline = blocks.CharBlock(
        help_text='Headline of this YouTube Regret'
    )

    image = ImageChooserBlock(
        required=False
    )

    imageAltText = blocks.CharBlock(
        required=False,
        help_text='Image description (for screen readers).'
    )

    story = blocks.TextBlock(
        verbose_name='youtube_regret_story',
        help_text='Story of this YouTube Regret',
    )

    class Meta:
        template = 'wagtailpages/blocks/youtube_regret_block.html'
