from django import forms
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock

from wagtailmedia import blocks as wagtailmedia_blocks


class RadioSelectBlock(blocks.ChoiceBlock):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.field.widget = forms.RadioSelect(
            choices=self.field.widget.choices
        )


class ExternalVideoBlock(blocks.StructBlock):
    video_url = blocks.URLBlock(
        help_text='For YouTube: go to your YouTube video and click “Share,” '
                  'then “Embed,” and then copy and paste the provided URL only. '
                  'For example: https://www.youtube.com/embed/3FIVXBawyQw '
                  'For Vimeo: follow similar steps to grab the embed URL. '
                  'For example: https://player.vimeo.com/video/9004979'
    )
    thumbnail = ImageChooserBlock(
        help_text='The image to show before the video is played.'
    )

    class Meta:
        icon = 'media'


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
    video_width = RadioSelectBlock(
        choices=(
            ("normal", "Normal"),
            ("wide", "Wide"),
            ("full_width", "Full Width"),
        ),
        default='normal',
        help_text='Wide videos are col-12, Full-Width videos reach both ends of the screen.'
    )

    class Meta:
        template = 'wagtailpages/blocks/video_block.html'


class WagtailVideoChooserBlock(wagtailmedia_blocks.VideoChooserBlock):
    class Meta:
        icon = 'media'
        template = 'wagtailpages/blocks/wagtail_video_block.html'
