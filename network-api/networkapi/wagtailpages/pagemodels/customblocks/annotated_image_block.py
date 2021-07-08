from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList
from wagtail.core import blocks
from .image_block import ImageBlock


class AnnotatedImageBlock(ImageBlock):
    caption = blocks.CharBlock(
        required=False
    )
    captionURL = blocks.CharBlock(
        required=False,
        help_text='Optional URL that this caption should link out to.'
    )
    wide_image = blocks.BooleanBlock(
        required=False,
        default=False,
        help_text='Would you like to use a wider image on desktop?'
    )
    full_width_image = blocks.BooleanBlock(
        required=False,
        default=False,
        help_text='Would you like to use a full width image? (Please use 16:9 image for best results)',
    )

    class Meta:
        icon = 'image'
        template = 'wagtailpages/blocks/annotated_image_block.html'
        help_text = 'Design Guideline: Please crop images to a 16:6 aspect ratio when possible.'

    def clean(self, value):
        errors = {}

        if value.get("wide_image") and value.get("full_width_image"):
            errors["wide_image"] = ErrorList(["Please select only one width option."])
            errors["full_width_image"] = ErrorList(
                ["Please select only one width option."]
            )

        if errors:
            raise ValidationError("Validation error in StructBlock", params=errors)

        return super().clean(value)
