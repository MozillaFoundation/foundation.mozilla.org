from wagtail.core import blocks
from wagtail_footnotes.blocks import RichTextBlockWithFootnotes
from wagtail.images.blocks import ImageChooserBlock


class ArticleRichText(RichTextBlockWithFootnotes):

    class Meta:
        label = "Content"


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
