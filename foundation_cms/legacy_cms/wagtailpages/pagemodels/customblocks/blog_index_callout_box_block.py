from wagtail import blocks
from wagtail.snippets import blocks as snippet_blocks
from wagtailmedia.blocks import AudioChooserBlock

from legacy_cms.wagtailpages.pagemodels.blog.blog_topic import BlogPageTopic
from legacy_cms.wagtailpages.pagemodels.customblocks.base_rich_text_options import (
    base_rich_text_options,
)
from legacy_cms.wagtailpages.pagemodels.customblocks.link_block import LinkBlock


class BlogIndexCalloutBoxBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        help_text="Heading for the callout box.",
    )

    related_topics = blocks.ListBlock(
        snippet_blocks.SnippetChooserBlock(BlogPageTopic),
        max_num=2,
        help_text="Optional topics to display at the top of the callout box.",
    )

    show_icon = blocks.BooleanBlock(
        required=False,
        help_text="Check this if you would like to render the headphone icon.",
    )

    body = blocks.RichTextBlock(
        help_text="Body text for the callout box.",
        features=base_rich_text_options,
        required=False,
    )

    audio = AudioChooserBlock(
        help_text="Optional audio player that will appear after the body.",
        required=False,
    )

    link_button = blocks.ListBlock(
        LinkBlock(), min_num=0, max_num=1, help_text="Optional Link Button for the callout box."
    )

    class Meta:
        template = "wagtailpages/blocks/blog_index_callout_box.html"
