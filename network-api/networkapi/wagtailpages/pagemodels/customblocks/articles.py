from wagtail.core import blocks


class ArticleRichText(blocks.RichTextBlock):

    class Meta:
        label = "Content"
        template = 'wagtailpages/blocks/article_richtext_block.html'
