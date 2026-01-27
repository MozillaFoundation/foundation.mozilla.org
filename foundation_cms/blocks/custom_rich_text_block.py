from wagtail.blocks import RichTextBlock


class CustomRichTextBlock(RichTextBlock):
    class Meta:
        template = "patterns/blocks/themes/default/rich_text_block.html"
        label = "Rich Text"
