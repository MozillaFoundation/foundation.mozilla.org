from wagtail import blocks
from wagtail.snippets.blocks import SnippetChooserBlock


class TicketsBlock(blocks.StructBlock):
    heading = blocks.CharBlock(help_text="Heading for the block.", required=False)
    tickets = blocks.ListBlock(SnippetChooserBlock("mozfest.Ticket"), max_num=3)

    class Meta:
        icon = "tag"
        label = "Tickets"
        template = "fragments/blocks/tickets_block.html"
