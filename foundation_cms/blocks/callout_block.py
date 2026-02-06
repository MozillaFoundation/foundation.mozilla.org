from foundation_cms.base.models.base_block import BaseBlock
from foundation_cms.blocks.custom_rich_text_block import CustomRichTextBlock


class CalloutBlock(BaseBlock):

    heading = CustomRichTextBlock(required=True, features=["h4", "h5", "h6"], help_text="Callout box title")
    description = CustomRichTextBlock(required=True, help_text="Callout box content")

    class Meta:
        icon = "help"
        label = "Callout Box"
        template_name = "callout_block.html"
