from wagtail.blocks import RichTextBlock

from foundation_cms.base.models.base_block import BaseBlock

from .custom_rich_text_block import CustomRichTextBlock


class CalloutBlock(BaseBlock):

    heading = CustomRichTextBlock(
        required=True, features=["h4", "h5", "h6"], label="Heading", help_text="Callout box title"
    )
    description = CustomRichTextBlock(required=True, label="Description", help_text="Callout box content")

    class Meta:
        icon = "help"
        label = "Callout Box"
        template_name = "callout_block.html"
