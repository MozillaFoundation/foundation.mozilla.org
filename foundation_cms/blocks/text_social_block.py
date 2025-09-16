from wagtail import blocks

from foundation_cms.base.models.base_block import BaseBlock


class TextSocialBlock(BaseBlock):

    title = blocks.CharBlock(required=True)
    text = blocks.RichTextBlock(required=False)

    class Meta:
        icon = "doc-full"
        label = "Text & Social Block"
        template_name = "text_social_block.html"
