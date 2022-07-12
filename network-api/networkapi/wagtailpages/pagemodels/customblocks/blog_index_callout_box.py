from wagtail.core import blocks
from ..customblocks.base_rich_text_options import base_rich_text_options
from wagtailmedia.blocks import AudioChooserBlock
from ..blog.blog_topic import BlogPageTopic
from django import forms 


class BlogIndexCalloutBlock(blocks.StructBlock):

    topics = blocks.MultipleChoiceBlock(
        label='Related Topics',
        choices=BlogPageTopic.get_topics(),
        help_text='',
        widget = forms.CheckboxSelectMultiple,
        max_num=2
    )

    show_icon = blocks.BooleanBlock(
        required=False,
        help_text='Check this if you would like to render the headphone icon.',
    )

    title = blocks.CharBlock(
        help_text='Heading for the Callout block'
    )

    body = blocks.RichTextBlock(
        label="Body text for the callout block",
        features=base_rich_text_options
    )

    audio = AudioChooserBlock()

    cta_button_text = blocks.CharBlock(
        help_text='Label text for the cta button'
    )
    
    # We use a char block because UrlBlock does not
    # allow for relative linking.
    cta_button_url = blocks.CharBlock()


    class Meta:
        template = "wagtailpages/blocks/blog_index_callout_box.html"