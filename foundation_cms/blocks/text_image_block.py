from wagtail import blocks
from foundation_cms.base.models.base_block import BaseBlock
from .image_block import CustomImageBlock
from modelcluster.contrib.taggit import ClusterTaggableManager


class TextImageBlock(BaseBlock):

    title = blocks.CharBlock()
    text = blocks.RichTextBlock()
    image = CustomImageBlock(required=False)
    link = blocks.URLBlock()
    tags = ClusterTaggableManager(through="base.TaggedPage", blank=True)


    class Meta:
        icon = "image"
        template = "patterns/blocks/image_block.html"