from wagtail import blocks
from wagtail.images.blocks import ImageBlock


class TabCardSetBlock(blocks.StructBlock):

    title = blocks.CharBlock()
    image = ImageBlock()
    subtitle = blocks.CharBlock()

    class Meta:
        icon = "form"
        template = "patterns/blocks/tab_card_set_block.html"
        label = "Tab Card Set"
