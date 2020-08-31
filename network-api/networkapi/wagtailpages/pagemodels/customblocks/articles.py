from wagtail.core import blocks
from wagtail_footnotes.blocks import RichTextBlockWithFootnotes


class ArticleRichText(RichTextBlockWithFootnotes):

    class Meta:
        label = "Content"
