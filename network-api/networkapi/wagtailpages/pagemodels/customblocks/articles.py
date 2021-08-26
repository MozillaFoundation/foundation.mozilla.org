from wagtail.core import blocks
from wagtail_footnotes.blocks import RichTextBlockWithFootnotes
from wagtail.images.blocks import ImageChooserBlock


class ArticleRichText(RichTextBlockWithFootnotes):

    class Meta:
        label = "Content"
        template = 'wagtailpages/blocks/rich_text_block.html'


class ArticleDoubleImageBlock(blocks.StructBlock):

    image_1 = ImageChooserBlock()
    image_1_caption = blocks.RichTextBlock(
        label="Image caption",
        required=False,
        features=['italic', 'bold', 'link'],
    )
    image_2 = ImageChooserBlock()
    image_2_caption = blocks.RichTextBlock(
        label="Image caption",
        required=False,
        features=['italic', 'bold', 'link'],
    )

    class Meta:
        label = "2x Images"
        template = "wagtailpages/blocks/article_double_image_block.html"


class ArticleFullWidthImageBlock(blocks.StructBlock):

    image = ImageChooserBlock()
    image_height = blocks.IntegerBlock(
        default=410,
        help_text='A custom height for this image. The image will be 1400px wide '
                  'by this height. Note: This may cause images to look pixelated. '
                  'If the browser is wider than 1400px the height will scale vertically '
                  'while the width scales horizontally'
    )
    caption = blocks.RichTextBlock(
        label="Image caption",
        required=False,
        features=['italic', 'bold', 'link'],
    )

    class Meta:
        label = "Wide Image"
        template = "wagtailpages/blocks/article_full_width_image_block.html"


class ArticleImageBlock(blocks.StructBlock):

    image = ImageChooserBlock()
    caption = blocks.RichTextBlock(
        label="Image caption",
        required=False,
        features=['italic', 'bold', 'link'],
    )
    alt_text = blocks.CharBlock(required=False)
    wide_image = blocks.BooleanBlock(
        required=False,
        default=False,
        help_text='Checking this will use a wider version of this image, but not full width. '
                  'For an edge-to-edge image, use the "Wide Image" block.'
    )

    class Meta:
        label = "Image"
        template = "wagtailpages/blocks/article_image_block.html"
