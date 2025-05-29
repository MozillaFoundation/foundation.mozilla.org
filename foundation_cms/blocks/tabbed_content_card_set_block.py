from wagtail import blocks
from wagtail.images.blocks import ImageBlock
from foundation_cms.base.models.base_block import BaseBlock


class TabbedContentCardSetBlock(BaseBlock):

    title = blocks.CharBlock()
    image = ImageBlock()
    subtitle = blocks.CharBlock()

    class Meta:
        icon = "form"
        template_name = "tabbed_content_card_set_block.html"
        label = "Tab Card Set"
