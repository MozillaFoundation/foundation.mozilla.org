from django import forms
from wagtail.core import blocks


class RadioSelectBlock(blocks.ChoiceBlock):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.field.widget = forms.RadioSelect(
            choices=self.field.widget.choices
        )


class iFrameBlock(blocks.StructBlock):
    url = blocks.CharBlock(
        help_text='Please note that only URLs from allow-listed domains will work.'
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
    iframe_width = RadioSelectBlock(
        choices=(
            ("normal", "Normal"),
            ("wide", "Wide"),
            ("full_width", "Full Width"),
        ),
        default='normal',
        help_text='Wide iframes are col-12, Full-Width iframes reach both ends of the screen'
    )
    disable_scroll = blocks.BooleanBlock(
        required=False,
        default=False,
        help_text='Checking this will add "scrolling=no" to the iframe. '
                  'Use this if your iframe is rendering an unnecessary scroll bar or whitespace below it.'
    )

    class Meta:
        template = 'wagtailpages/blocks/iframe_block.html'
