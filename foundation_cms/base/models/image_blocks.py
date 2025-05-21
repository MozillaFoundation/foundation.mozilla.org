from wagtail import blocks
from wagtail.images.blocks import ImageBlock


class SingleImageBlock(blocks.StructBlock):
    """
    A single image with title and orientation choice
    """
    title = blocks.CharBlock(required=True, help_text="Title for this image")
    image = ImageBlock(required=True)
    orientation = blocks.ChoiceBlock(
        choices=[
            ('portrait', 'Portrait'),
            ('landscape', 'Landscape'),
        ],
        default='landscape',
        help_text='Select the orientation of this image'
    )
    
    class Meta:
        icon = "image"
        template = "patterns/components/single_image_block.html"
        label = "Single Image"


class DoubleImageBlock(blocks.StructBlock):
    """
    Two images side by side, each with its own title and orientation
    """
    # First image
    first_title = blocks.CharBlock(required=True, help_text="Title for first image")
    first_image = ImageBlock(required=True)
    first_orientation = blocks.ChoiceBlock(
        choices=[
            ('portrait', 'Portrait'),
            ('landscape', 'Landscape'),
        ],
        default='landscape',
        help_text='Select the orientation of the first image'
    )
    
    # Second image
    second_title = blocks.CharBlock(required=True, help_text="Title for second image")
    second_image = ImageBlock(required=True)
    second_orientation = blocks.ChoiceBlock(
        choices=[
            ('portrait', 'Portrait'),
            ('landscape', 'Landscape'),
        ],
        default='landscape',
        help_text='Select the orientation of the second image'
    )
    
    class Meta:
        icon = "image"
        template = "patterns/components/double_image_block.html"
        label = "Double Image" 