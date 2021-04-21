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

    class Meta:
        icon = 'image'
        template = 'wagtailpages/blocks/annotated_image_block.html'
        help_text = 'Design Guideline: Please crop images to a 16:6 aspect ratio when possible.'
