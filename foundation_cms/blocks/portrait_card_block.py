from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

from foundation_cms.base.models.base_block import BaseBlock


class PortraitCardBlock(BaseBlock):
    label = blocks.CharBlock(
        required=False, max_length=36, label="Label", help_text="Appears above the headline (max 36 characters)."
    )
    headline = blocks.CharBlock(
        required=False, max_length=36, label="Headline", help_text="Appears as the main heading (max 36 characters)."
    )
    image = ImageChooserBlock(required=False, label="Image", help_text="Image should follow a 2:3 aspect ratio.")

    class Meta:
        label = "Portrait Card"
        icon = "form"
