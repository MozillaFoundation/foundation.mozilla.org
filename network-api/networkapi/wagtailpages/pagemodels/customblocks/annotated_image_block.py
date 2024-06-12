from django import forms
from wagtail import blocks

from .image_block import ImageBlock
from .link_block import LinkBlockWithoutLabel


class RadioSelectBlock(blocks.ChoiceBlock):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.field.widget = forms.RadioSelect(choices=self.field.widget.choices)


class AnnotatedImageBlock(ImageBlock):
    caption = blocks.CharBlock(required=False)
    caption_url = blocks.ListBlock(
        LinkBlockWithoutLabel(), min_num=0, max_num=1, help_text="Optional URL that this caption should link out to."
    )
    image_width = RadioSelectBlock(
        choices=(
            ("normal", "Normal"),
            ("wide", "Wide"),
            ("full_width", "Full Width"),
        ),
        default="normal",
        help_text="Wide images are col-12, Full-Width Images reach both ends of the screen "
        "(16:6 images recommended for full width)",
    )

    class Meta:
        icon = "image"
        template = "wagtailpages/blocks/annotated_image_block.html"
        help_text = "Design Guideline: Please crop images to a 16:6 aspect ratio when possible."
