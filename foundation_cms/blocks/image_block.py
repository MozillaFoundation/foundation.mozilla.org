from wagtail.blocks import StructBlock, CharBlock, ChoiceBlock
from wagtail.images.blocks import ImageBlock

class CustomImageBlock(StructBlock):
    """
    A reusable image block with title and orientation options
    """
    title = CharBlock(required=True, help_text="Title/caption for this image")
    image = ImageBlock(required=True)
    orientation = ChoiceBlock(
        choices=[
            ('portrait', 'Portrait'),
            ('landscape', 'Landscape'),
        ],
        default='landscape',
        help_text='Select the orientation of this image'
    )
    
    class Meta:
        icon = "image"
        template = "patterns/blocks/image_block.html"
        label = "Image" 