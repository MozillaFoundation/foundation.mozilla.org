from wagtail.core import blocks
from wagtail.snippets import blocks as snippet_blocks
from ..customblocks.base_rich_text_options import base_rich_text_options
from wagtailmedia.blocks import AudioChooserBlock
from ..blog.blog_topic import BlogPageTopic
from django import forms


class BlogIndexCalloutBlock(blocks.StructBlock):

    title = blocks.CharBlock(
        help_text='Heading for the Callout Box'
    )

    related_topics = blocks.ListBlock(
        snippet_blocks.SnippetChooserBlock(BlogPageTopic), 
        max_num=2,
        help_text='Optional topics to display at the top of the callout box.'

        )

    show_icon = blocks.BooleanBlock(
        required=False,
        help_text='Check this if you would like to render the headphone icon.',
    )

    body = blocks.RichTextBlock(
        help_text="Body text for the callout block",
        features=base_rich_text_options,
        required=False
    )

    audio = AudioChooserBlock(
        help_text='Optional audio that can be played from the callout box.',
        required=False
        )

    link_button_text = blocks.CharBlock(
        help_text='Label text for the link button',
        required=False
    )

    # We use a char block because UrlBlock does not
    # allow for relative linking.
    link_button_url = blocks.CharBlock(
        help_text="URL that the button should link out to.",
        required=False
        )

    class Meta:
        template = "wagtailpages/blocks/blog_index_callout_box.html"
