from wagtail.blocks import CharBlock, ChoiceBlock, StreamBlock
from wagtail.images.blocks import ImageBlock

from foundation_cms.base.models.base_block import BaseBlock
from foundation_cms.blocks.custom_rich_text_block import CustomRichTextBlock
from foundation_cms.blocks.link_block import OptionalLinkBlock


class ImageCarouselItemBlock(BaseBlock):
    image = ImageBlock(required=True, help_text="Select an image for this item.")
    header = CharBlock(
        required=False,
        max_length=80,
        help_text="Optional header text shown above the image item.",
    )
    title = CharBlock(
        required=False,
        max_length=120,
        help_text="Optional title for the image item (e.g. speaker name or event title).",
    )
    description = CustomRichTextBlock(
        required=False,
        help_text="Optional rich text description for the image item.",
    )
    link = OptionalLinkBlock(required=False, label="Link", help_text="Optional link for this item.")

    class Meta:
        icon = "image"
        label = "Carousel Item"
        template_name = "image_carousel_item_block.html"


class ImageCarouselBlock(BaseBlock):
    title = CharBlock(required=False, help_text="Optional title for the carousel container.")
    orientation = ChoiceBlock(
        choices=[
            ("portrait", "Portrait"),
            ("landscape", "Landscape"),
        ],
        default="portrait",
        required=True,
        label="Orientation",
        help_text="Select the orientation for carousel items.",
    )

    items = StreamBlock(
        [
            ("carousel_item", ImageCarouselItemBlock()),
        ],
        max_num=10,
        help_text="Items to display in the carousel. Maximum of 10 items.",
    )

    class Meta:
        icon = "list-ul"
        label = "Image Carousel"
        template_name = "image_carousel_block.html"
