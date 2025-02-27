from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class ImageFeatureBlock(blocks.StructBlock):
    image = ImageChooserBlock()

    alt_text = blocks.CharBlock(help_text="Image description (for screen readers).")
    metadata = blocks.CharBlock(required=False)
    title = blocks.CharBlock(help_text="Heading for the card.")
    title_link = blocks.PageChooserBlock(help_text="Page that the title should link out to.", required=False)
    body = blocks.CharBlock(required=False)

    class Meta:
        icon = "image"
        template = "wagtailpages/blocks/image_feature_block.html"
