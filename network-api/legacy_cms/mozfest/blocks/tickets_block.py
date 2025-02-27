from wagtail import blocks
from wagtail.snippets.blocks import SnippetChooserBlock

from legacy_cms.wagtailpages import utils


class TicketsBlock(blocks.StructBlock):
    heading = blocks.CharBlock(help_text="Heading for the block.", required=False)
    tickets = blocks.ListBlock(SnippetChooserBlock("mozfest.Ticket"), max_num=3)

    class Meta:
        icon = "tag"
        label = "Tickets"
        template = "fragments/blocks/tickets_block.html"

    def get_context(self, request, parent_context=None):
        context = super().get_context(request, parent_context=parent_context)
        request_language_code = utils.get_language_from_request(context["request"])
        context["tito_widget_lang_code"] = utils.map_language_code_to_tito_supported_language_code(
            request_language_code,
        )
        return context
