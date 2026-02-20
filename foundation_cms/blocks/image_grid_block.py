from wagtail.blocks import CharBlock, ChoiceBlock, ListBlock, RichTextBlock, StructBlock
from wagtail.images.blocks import ImageBlock

from foundation_cms.base.models.base_block import BaseBlock
from foundation_cms.blocks.link_block import OptionalLinkBlock


class ImageGridItemBlock(StructBlock):
    """Individual grid item"""

    image = ImageBlock(required=True)
    caption = RichTextBlock(
        required=False, features=["h5", "h6", "large", "bold", "italic"], help_text="Optional caption for this image"
    )
    link = OptionalLinkBlock(required=False, help_text="Optional link for both image and caption")

    class Meta:
        icon = "image"
        label = "Grid Item"


class ImageGridSectionBlock(StructBlock):
    """Individual section with items"""

    heading = CharBlock(required=False, help_text="Optional heading for this section", max_length=100)
    section_orientation = ChoiceBlock(
        choices=[
            ("portrait", "Portrait"),
            ("landscape", "Landscape"),
            ("square", "Square"),
        ],
        default="landscape",
        help_text="Orientation for all images in this section",
        label="Image grid section orientation",
    )
    items_per_row = ChoiceBlock(
        choices=[
            ("4", "4 per row"),
            ("5", "5 per row"),
            ("6", "6 per row"),
        ],
        default="4",
        label="Items per section row",
    )
    items = ListBlock(ImageGridItemBlock(), min_num=1)

    class Meta:
        icon = "grip"
        label = "Image Grid Section"


class ImageGridBlock(BaseBlock):
    """Main container block for image grid with multiple sections"""

    sections = ListBlock(ImageGridSectionBlock(), min_num=1, label="Image grid sections")

    class Meta:
        icon = "grip"
        label = "Image Grid"
        template_name = "image_grid_block.html"
