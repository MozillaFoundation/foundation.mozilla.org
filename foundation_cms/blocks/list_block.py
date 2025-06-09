from wagtail import blocks


class ListBlock(blocks.StructBlock):
    """
    A block for rendering a list of items.
    """
    title = blocks.CharBlock(help_text="Heading displayed above the list")
    description = blocks.TextBlock(help_text="Description displayed above the list")
    items = blocks.ListBlock(
       blocks.PageChooserBlock(), 
        min_num=1, 
        max_num=4,
    )
    
    class Meta:
        template_name = "list_block.html"
        icon = "list-ul"
        label = "List" 