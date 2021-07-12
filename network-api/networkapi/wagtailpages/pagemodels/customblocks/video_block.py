from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList
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
    wide_video = blocks.BooleanBlock(
        required=False,
        default=False,
        help_text='Would you like to use a wider video on desktop?'
    )
    full_width_video = blocks.BooleanBlock(
        required=False,
        default=False,
        help_text='Would you like to use a full width video?',
    )

    class Meta:
        template = 'wagtailpages/blocks/video_block.html'


    def clean(self, value):
        errors = {}

        if value.get("wide_video") and value.get("full_width_video"):
            errors["wide_video"] = ErrorList(["Please select only one width option."])
            errors["full_width_video"] = ErrorList(
                ["Please select only one width option."]
            )

        if errors:
            raise ValidationError("Validation error in StructBlock", params=errors)

        return super().clean(value)
