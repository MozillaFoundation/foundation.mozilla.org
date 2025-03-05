from wagtail import blocks
from wagtail.snippets.blocks import SnippetChooserBlock

from foundation_cms.legacy_apps.wagtailpages.utils import (
    get_language_from_request,
    map_language_code_to_tito_supported_language_code,
)


class TitoWidgetBlock(blocks.StructBlock):
    button_label = blocks.CharBlock(help_text="The text to show on the Tito button.")
    styling = blocks.ChoiceBlock(
        choices=[
            ("btn-primary", "Primary button"),
            ("btn-secondary", "Secondary button"),
        ],
        default="btn-primary",
    )
    event = SnippetChooserBlock("events.TitoEvent", help_event="The Tito event to be displayed")
    releases = blocks.CharBlock(
        required=False,
        help_text='Comma-separated list of ticket/release IDs to limit to, e.g. "3elajg6qcxu,6qiiw4socs4"',
    )

    class Meta:
        icon = "form"
        template = "wagtailpages/blocks/tito_widget_block.html"

    def get_context(self, request, parent_context=None):
        context = super().get_context(request, parent_context=parent_context)
        request_language_code = get_language_from_request(context["request"])
        context["tito_widget_lang_code"] = map_language_code_to_tito_supported_language_code(request_language_code)
        return context
