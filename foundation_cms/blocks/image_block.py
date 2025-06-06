from wagtail.blocks import CharBlock, ChoiceBlock
from wagtail.images.blocks import ImageBlock

from foundation_cms.base.models.base_block import BaseBlock


class CustomImageBlock(BaseBlock):
    """
    A reusable image block with title and orientation options
    """

    title = CharBlock(required=False, help_text="Title/caption for this image")
    image = ImageBlock(required=True)
    orientation = ChoiceBlock(
        choices=[
            ("portrait", "Portrait"),
            ("landscape", "Landscape"),
            ("square", "Square"),
        ],
        default="landscape",
        help_text="Select the orientation of this image",
    )

    class Meta:
        icon = "image"
        template_name = "image_block.html"
        label = "Image"
