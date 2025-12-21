from wagtail import blocks

from foundation_cms.base.models.base_block import BaseBlock


class PodcastBlock(BaseBlock):
    title = blocks.CharBlock(
        help_text=(
            'Title of the podcast. '
            '<strong>Note:</strong> Does not render on "NothingPersonal" pages.'
        )
    )
    description = blocks.TextBlock(
        required=False,
        help_text=(
            'Optional short description of the podcast. '
            '<strong>Note:</strong> Does not render on "NothingPersonal" pages.'
        ),
    )
    simplecast_embed_code = blocks.CharBlock()

    class Meta:
        icon = "media"
        template_name = "podcast_block.html"
        label = "Podcast Block"
