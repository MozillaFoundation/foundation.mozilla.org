from wagtail.images.blocks import ImageChooserBlock

from .base_card_block import BaseCardBlock


class SpotlightCardBlock(BaseCardBlock):

    image = ImageChooserBlock(required=False, label="Image", help_text="Image should follow a 1:1 aspect ratio.")

    class Meta:
        label = "Spotlight Card"
        icon = "form"
