from wagtail.blocks import RichTextBlock

DEFAULT_RICH_TEXT_FEATURES = [
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "bold",
    "italic",
    "large",
    "ol",
    "ul",
    "hr",
    "embed",
    "link",
    "document-link",
    "image",
]


class CustomRichTextBlock(RichTextBlock):
    def __init__(self, **kwargs):
        kwargs["features"] = DEFAULT_RICH_TEXT_FEATURES
        super().__init__(**kwargs)

    class Meta:
        template = "patterns/blocks/themes/default/rich_text_block.html"
        label = "Rich Text"
