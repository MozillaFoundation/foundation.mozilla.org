from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList
from wagtail.core import blocks


class iFrameBlock(blocks.StructBlock):
    url = blocks.CharBlock(
        help_text='Please note that only URLs from white-listed domains will work.'
    )
    height = blocks.IntegerBlock(
        required=False,
        help_text='Optional integer pixel value for custom iFrame height'
    )
    caption = blocks.CharBlock(
        required=False
    )
    captionURL = blocks.CharBlock(
        required=False,
        help_text='Optional URL that this caption should link out to.'
    )
    wide_iframe = blocks.BooleanBlock(
        required=False,
        help_text='Check this box for a wider iframe',
    )
    full_width_iframe = blocks.BooleanBlock(
        required=False,
        default=False,
        help_text='Would you like to use a full width iframe?',
    )

    class Meta:
        template = 'wagtailpages/blocks/iframe_block.html'

    def clean(self, value):
        errors = {}

        if value.get("wide_iframe") and value.get("full_width_iframe"):
            errors["wide_iframe"] = ErrorList(["Please select only one width option."])
            errors["full_width_iframe"] = ErrorList(
                ["Please select only one width option."]
            )

        if errors:
            raise ValidationError("Validation error in StructBlock", params=errors)

        return super().clean(value)
