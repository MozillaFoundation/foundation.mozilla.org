from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class DearInternetLetterBlock(blocks.StructBlock):
    author_name = blocks.CharBlock()

    author = blocks.RichTextBlock(
        features=[
            'bold', 'italic', 'link',
        ],
        help_text='Author description'
    )

    author_photo = ImageChooserBlock(
        required=False
    )

    letter = blocks.RichTextBlock(
        features=[
            'bold', 'link', 'ol', 'ul',
        ],
        help_text='Main letter content'
    )

    image = ImageChooserBlock(
        required=False
    )

    video_url = blocks.URLBlock(
        help_text="Video url to link out to",
        required=False
    )

    class Meta:
        template = 'wagtailpages/blocks/dear_internet_letter_block.html'
