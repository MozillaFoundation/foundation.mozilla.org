from wagtail import blocks

from foundation_cms.base.models.base_block import BaseBlock
from foundation_cms.blocks.custom_rich_text_block import CustomRichTextBlock


class TextSocialBlock(BaseBlock):

    title = blocks.CharBlock(required=False)
    text = CustomRichTextBlock(required=False)

    class Meta:
        icon = "doc-full"
        label = "Text & Social Block"
        template_name = "text_social_block.html"
