from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class DearInternetLetterBlock(blocks.StructBlock):
    author_name = blocks.CharBlock()

    author_description = blocks.RichTextBlock(
        features=[
            'bold', 'italic', 'link',
        ],
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
        help_text="Video url to link out to. "
                  "Note that video embed will show only when the url is a valid YouTube video embed url. "
                  "Go to your YouTube video and click “Share,” "
                  "then “Embed,” and then copy and paste the provided URL only. "
                  "For example: https://www.youtube.com/embed/s7OD5BgFrVM",
        required=False
    )

    class Meta:
        template = 'wagtailpages/blocks/dear_internet_letter_block.html'
