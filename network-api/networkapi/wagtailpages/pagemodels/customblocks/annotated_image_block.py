from wagtail.core import blocks
from wagtail_localize.fields import SynchronizedField
from .image_block import ImageBlock


class AnnotatedImageBlock(ImageBlock):
    caption = blocks.CharBlock(
        required=False
    )

    captionURL = blocks.URLBlock(
        required=False,
        help_text='Optional URL that this caption should link out to.'
    )

    override_translatable_fields = [
        SynchronizedField('captionURL'),
    ]

    class Meta:
        icon = 'image'
        template = 'wagtailpages/blocks/annotated_image_block.html'
        help_text = 'Design Guideline: Please crop images to a 16:6 aspect ratio when possible.'
