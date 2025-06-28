from wagtail import blocks

from foundation_cms.base.models.base_block import BaseBlock


class ListBlock(BaseBlock):
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
        icon = "list-ul"
        template_name = "list_block.html"
        label = "List Block"
