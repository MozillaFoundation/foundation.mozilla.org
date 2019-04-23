from wagtail.images.blocks import ImageChooserBlock
from wagtail.core import blocks

from .air_table_block import AirTableBlock
from .bootstrap_spacer import BootstrapSpacerBlock
from .iframe_block import iFrameBlock
from .annotated_image_block import AnnotatedImageBlock
from .image_grid_block import ImageGridBlock
from .image_text_mini import ImageTextMini, ImageBlock
from .image_text import ImageTextBlock
from .latest_profile_list import LatestProfileQueryValue, LatestProfileList
from .link_button import LinkButtonBlock
from .profile_by_id import ProfileById
from .profile_directory import ProfileDirectory
from .pulse_project_list import PulseProjectList
from .quote_block import QuoteBlock
from .video_block import VideoBlock

__all__ = [
    'AirTableBlock',
    'BootstrapSpacerBlock',
    'iFrameBlock',
    'AnnotatedImageBlock',
    'ImageGridBlock',
    'ImageTextMini',
    'ImageTextBlock',
    'LatestProfileQueryValue',
    'LatestProfileList',
    'LinkButtonBlock',
    'ProfileById',
    'ProfileDirectory',
    'PulseProjectList',
    'QuoteBlock',
    'VideoBlock'
]

# Deprecated/ Unused ?


class FigureBlock2(blocks.StructBlock):
    image = ImageChooserBlock()
    caption = blocks.CharBlock(
        required=False,
        help_text='Please remember to properly attribute any images we use.'
    )
    url = blocks.CharBlock(
        required=False,
        help_text='Optional URL that this figure should link out to.',
    )
    square_image = blocks.BooleanBlock(
        default=True,
        required=False,
        help_text='If left checked, the image will be cropped to be square.'
    )


class AlignedImageBlock(ImageBlock):
    alignment = blocks.ChoiceBlock(
        choices=[
            ('', 'Do not apply any explicit alignment classes.'),
            ('left-align', 'Left-align this image with the page content.'),
            ('right-align', 'Right-align this image with the page content.'),
            ('center', 'Center this image with the page content.'),
            ('full-width', 'Make this image full-width.'),
        ],
        default='',
        required=False
    )

    class Meta:
        icon = 'image'
        template = 'wagtailpages/blocks/aligned_image_block.html'
