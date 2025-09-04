from django import forms
from wagtail import blocks

from foundation_cms.base.models.base_block import BaseBlock


class RadioSelectBlock(blocks.ChoiceBlock):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.field.widget = forms.RadioSelect(choices=self.field.widget.choices)


class iFrameBlock(BaseBlock):
    url = blocks.CharBlock(help_text="Please note that only URLs from allow-listed domains will work.")
    height = blocks.IntegerBlock(
        required=False,
        help_text="Optional integer pixel value for custom iFrame height",
    )
    iframe_width = RadioSelectBlock(
        choices=(
            ("normal", "Normal"),
            ("full_width", "Full Width"),
        ),
        default="normal",
    )
    disable_scroll = blocks.BooleanBlock(
        required=False,
        default=False,
        help_text='Checking this will add "scrolling=no" to the iframe. '
        "Use this if your iframe is rendering an unnecessary scroll bar or whitespace below it.",
    )

    class Meta:
        template_name = "iframe_block.html"
