from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

from foundation_cms.base.models.base_block import BaseBlock

from .link_block import OptionalLinkBlock


class BaseCardBlock(BaseBlock):
    label = blocks.CharBlock(
        required=False, max_length=50, label="Label", help_text="Appears above the headline (max 36 characters)."
    )
    headline = blocks.CharBlock(
        required=False, max_length=50, label="Headline", help_text="Appears as the main heading (max 36 characters)."
    )
    image = ImageChooserBlock(required=False, label="Image", help_text="Image should follow a 2:3 aspect ratio.")
    cta_link = OptionalLinkBlock(required=False, label="Call to Action Link", help_text="Optional link for the card.")

    class Meta:
        label = "Base Card"
        icon = "form"
