from wagtail.images.blocks import ImageBlock
from wagtail.blocks import CharBlock, RichTextBlock

from foundation_cms.base.models.base_block import BaseBlock


class SpotlightCardBlock(BaseBlock):

    title = CharBlock(required=False)
    label = CharBlock(required=False, max_length=50, label="Label")
    description = RichTextBlock(required=False, max_length=500, label="Description")
    image = ImageBlock(required=False, label="Image", help_text="Image should follow a 1:1 aspect ratio.")

    class Meta:
        label = "Spotlight Card"
        icon = "form"
