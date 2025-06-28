from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

from foundation_cms.base.models.base_block import BaseBlock

from .link_block import OptionalLinkBlock


class BaseCardBlock(BaseBlock):
    label = blocks.CharBlock(required=False, label="Label", help_text="Appears above the headline.")
    headline = blocks.CharBlock(required=False, label="Headline", help_text="Appears as the main heading.")
    image = ImageChooserBlock(required=False, label="Image", help_text="Optional Image for the card")
    cta_link = OptionalLinkBlock(required=False, label="Call to Action Link", help_text="Optional link for the card.")

    class Meta:
        label = "Base Card"
        icon = "form"
