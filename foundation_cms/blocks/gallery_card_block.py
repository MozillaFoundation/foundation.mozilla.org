from wagtail.blocks import PageChooserBlock

from foundation_cms.base.models.base_block import BaseBlock


class GalleryCardBlock(BaseBlock):
    """
    A simple card block to display projects in a gallery
    """

    page = PageChooserBlock(required=True, page_type="gallery_hub.ProjectPage", label="Page")

    class Meta:
        label = "Gallery Card"
        icon = "image"
        template_name = "gallery_card_block.html"
