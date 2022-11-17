from wagtail.core import blocks
from wagtail.snippets.blocks import SnippetChooserBlock


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
