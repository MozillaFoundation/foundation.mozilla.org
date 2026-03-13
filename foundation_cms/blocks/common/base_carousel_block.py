from wagtail.blocks import CharBlock, ChoiceBlock
from wagtail.images.blocks import ImageChooserBlock

from foundation_cms.base.models.base_block import BaseBlock
from foundation_cms.blocks.link_block import OptionalLinkBlock


class BaseCarouselItemBlock(BaseBlock):
    """
    Base block for carousel items, with common fields like image and link.
    Specific carousel item types can extend this base block to add their own unique fields."""

    image = ImageChooserBlock(required=True, help_text="Select an image for this item.")
    link = OptionalLinkBlock(required=False, help_text="Optional link for this item.")

    class Meta:
        abstract = True


class BaseCarouselBlock(BaseBlock):
    """
    Base block for carousel containers, with common fields like title and orientation.
    Specific carousel types can extend this base block to add their own unique fields.
    """

    title = CharBlock(required=False, help_text="Optional title for the container.")
    orientation = ChoiceBlock(
        choices=[
            ("portrait", "Portrait"),
            ("landscape", "Landscape"),
        ],
        default="portrait",
        required=True,
        label="Item Orientation",
        help_text="Select the orientation for the carousel items.",
    )

    class Meta:
        abstract = True
