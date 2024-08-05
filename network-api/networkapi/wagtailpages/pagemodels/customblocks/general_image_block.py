from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from .link_block import LinkWithoutLabelBlock

from ..customblocks.base_rich_text_options import base_rich_text_options

class RadioSelectBlock(blocks.ChoiceBlock):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.field.widget = forms.RadioSelect(choices=self.field.widget.choices)

class GeneralImageBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    alt_text_required = blocks.CharBlock(required=True, help_text="Image description (for screen readers).")
    caption = blocks.RichTextBlock(
        label="Image caption",
        required=False,
        features=base_rich_text_options,
    )
    caption_url = blocks.ListBlock(
        LinkWithoutLabelBlock(), min_num=0, max_num=1, help_text="Optional URL that this caption should link out to."
    )
    alt_text = blocks.CharBlock(required=False)
    wide_image = blocks.BooleanBlock(
        required=False,
        default=False,
        help_text="Checking this will use a wider version of this image, but not full width. "
                  'For an edge-to-edge image, use the "Wide Image" block.',
    )
    image_height = blocks.IntegerBlock(
        default=410,
        help_text="A custom height for this image. The image will be 1400px wide "
                  "by this height. Note: This may cause images to look pixelated. "
                  "If the browser is wider than 1400px the height will scale vertically "
                  "while the width scales horizontally",
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

    body = blocks.StreamBlock([
        ('image_block', blocks.StructBlock([
            ('image', image),
            ('alt_text', alt_text_required),
        ])),
        ('article_image_block', blocks.StructBlock([
            ('image', image),
            ('caption', caption),
            ('alt_text', alt_text),
            ('wide_image', wide_image),
        ])),
        ('article_full_width_image_block', blocks.StructBlock([
            ('image', image),
            ('caption', caption),
            ('image_height', image_height),
        ])),
        ('article_double_image_block', blocks.StructBlock([
            ('image', image),
            ('image_2', image),
            ('caption', caption),
            ('caption_2', caption),
        ])),
        ('annotated_image_block', blocks.StructBlock([
            ('image', image),
            ('alt_text', alt_text_required),
            ('image_width', image_width),
            ('caption', caption),
            ('caption_url', caption_url),
        ])),
    ])
