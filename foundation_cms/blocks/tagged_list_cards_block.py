from wagtail import blocks


class TaggedListCardsBlock(blocks.StructBlock):
    """
    A block for rendering a grid of listing cards.
    """
    title = blocks.CharBlock(help_text="Heading displayed above the cards")
    cards = blocks.ListBlock(
       blocks.PageChooserBlock(), 
        min_num=1, 
        max_num=4,
    )
    
    class Meta:
        template_name = "tagged_list_cards_block.html"
        icon = "list-ul"
        label = "Tagged List Cards" 