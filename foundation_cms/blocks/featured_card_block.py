from wagtail.blocks import CharBlock
from wagtail.images.blocks import ImageBlock

from foundation_cms.base.models.base_block import BaseBlock
from foundation_cms.blocks.custom_rich_text_block import CustomRichTextBlock

from .link_button_block import LinkButtonBlock


class FeaturedCardBlock(BaseBlock):
    heading = CharBlock(required=True, max_length=50, label="Heading")
    description = CustomRichTextBlock(required=True, max_length=500, label="Description", features=["bold", "italic"])
    image = ImageBlock(required=True, label="Image", help_text="Image for the card")
    button = LinkButtonBlock(required=False, label="Button", help_text="Link button for the card.")

    class Meta:
        label = "Featured Card"
        icon = "form"
        template_name = "featured_card_block.html"
