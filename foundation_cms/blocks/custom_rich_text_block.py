from wagtail.blocks import RichTextBlock
from foundation_cms.constants import DEFAULT_RICH_TEXT_FEATURES


class CustomRichTextBlock(RichTextBlock):
    def __init__(self, **kwargs):
        kwargs["features"] = DEFAULT_RICH_TEXT_FEATURES
        super().__init__(**kwargs)

    class Meta:
        template = "patterns/blocks/themes/default/rich_text_block.html"
        label = "Rich Text"
