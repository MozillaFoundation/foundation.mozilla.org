from wagtail.blocks import CharBlock, RichTextBlock
from wagtail.images.blocks import ImageChooserBlock

from .link_block import OptionalLinkBlock

from foundation_cms.base.models.base_block import BaseBlock


class FeaturedCardBlock(BaseBlock):
    heading = CharBlock(required=True, max_length=50, label="Heading")
    description = RichTextBlock(required=True, max_length=500, label="Description", features=["bold", "italic"])
    image = ImageChooserBlock(required=True, label="Image", help_text="Image for the card")
    button = OptionalLinkBlock(
        required=False, label="Button", help_text="Button label and link for the card."
    )


    class Meta:
        label = "Featured Card"
        icon = "form"
        template_name = "featured_card_block.html"