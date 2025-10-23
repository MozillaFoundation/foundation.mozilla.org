from wagtail.blocks import CharBlock, RichTextBlock
from wagtail.images.blocks import ImageBlock

from foundation_cms.base.models.base_block import BaseBlock

from .decorators import skip_default_wrapper_on
from .link_button_block import LinkButtonBlock


@skip_default_wrapper_on("*")
class FeaturedCardBlock(BaseBlock):
    heading = CharBlock(required=True, max_length=50, label="Heading")
    description = RichTextBlock(required=True, max_length=500, label="Description", features=["bold", "italic"])
    image = ImageBlock(required=True, label="Image", help_text="Image for the card")
    button = LinkButtonBlock(required=False, label="Button", help_text="Link button for the card.")

    class Meta:
        label = "Featured Card"
        icon = "form"
        template_name = "featured_card_block.html"
