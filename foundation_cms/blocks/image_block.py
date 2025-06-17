from wagtail.blocks import CharBlock
from wagtail.images.blocks import ImageBlock

from foundation_cms.base.models.base_block import BaseBlock


class CustomImageBlock(BaseBlock):
    """
    A reusable image block with title
    """

    title = CharBlock(required=False, help_text="Title/caption for this image")
    image = ImageBlock(required=True)

    class Meta:
        icon = "image"
        template_name = "image_block.html"
        label = "Image"
