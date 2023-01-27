from django.conf import settings
from wagtail.core import blocks
from wagtail.snippets.blocks import SnippetChooserBlock

from networkapi.wagtailpages.utils import get_language_from_request


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
        language_code = get_language_from_request(request)
        context["lang_code"] = self.get_widget_language_code(language_code)

        return context

    def get_widget_language_code(self, language_code):
        default_language_code = settings.LANGUAGE_CODE
        tito_supported_language_codes = {"en", "de", "es", "fr", "nl", "pl"}

        if language_code in tito_supported_language_codes:
            return language_code
        else:
            return default_language_code
