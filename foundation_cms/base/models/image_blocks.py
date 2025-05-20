from wagtail import blocks
from wagtail.images.blocks import ImageBlock


class SizedImageBlock(blocks.StructBlock):
    """
    An image block with customizable size options and a title.
    """
    title = blocks.CharBlock(required=True, help_text="Title for this image")
    image = ImageBlock(required=True)
    
    size = blocks.ChoiceBlock(
        choices=[
            ('potrait', 'Potrait'),
            ('landscape', 'Landscape'),
            ('mixed', 'Mixed'),
            ('double', 'Double'),
        ],
        default='medium',
        help_text='Select the display size for this image'
    )
    
    class Meta:
        icon = "image"
        help_text = "An image with a title and customizable size" 