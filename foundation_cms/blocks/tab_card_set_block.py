from wagtail import blocks


class TabCardSetBlock(blocks.StructBlock):
    
    title = blocks.CharBlock()
    image = blocks.ImageBlock()
    subtitle = blocks.CharBlock()

    class Meta:
        icon = "form"
        template = "patterns/blocks/tab_card_set_block.html"
        label = "Tab Card Set"
