from wagtail.blocks import CharBlock, RichTextBlock
from wagtail.images.blocks import ImageBlock

from foundation_cms.base.models.base_block import BaseBlock


class SpotlightCardBlock(BaseBlock):

    title = CharBlock(required=True)
    name = CharBlock(required=True, max_length=50, label="Name")
    description = RichTextBlock(required=True, max_length=500, label="Description", features=["bold", "italic"])
    image = ImageBlock(required=True, label="Image", help_text="Image should follow a 1:1 aspect ratio.")

    class Meta:
        label = "Spotlight Card"
        icon = "form"
