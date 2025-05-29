from wagtail import blocks
from foundation_cms.base.models.base_block import BaseBlock
from .image_block import CustomImageBlock
from .link_block import LinkBlock
from modelcluster.contrib.taggit import ClusterTaggableManager


class TextImageBlock(BaseBlock):

    title = blocks.CharBlock(required=False)
    text = blocks.RichTextBlock(required=False)
    image = CustomImageBlock(required=False)
    link = LinkBlock()
    tags = ClusterTaggableManager(through="base.TaggedPage", blank=True)


    class Meta:
        icon = "image"
        template_name = "text_image_block.html"