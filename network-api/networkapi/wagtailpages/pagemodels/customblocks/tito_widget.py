from wagtail.core import blocks


class TitoWidgetBlock(blocks.StructBlock):
    button_label = blocks.CharBlock(help_text="The text to show on the Tito button.")
    styling = blocks.ChoiceBlock(
        choices=[
            ("btn-primary", "Primary button"),
            ("btn-secondary", "Secondary button"),
        ],
        default="btn-primary",
    )
    event = blocks.CharBlock(help_text='The ID of the event, e.g. "ultimateconf/2013"')
    releases = blocks.CharBlock(
        required=False,
        help_text='Comma-separated list of ticket/release IDs to limit to, e.g. "3elajg6qcxu,6qiiw4socs4"',
    )
    redirect_page = blocks.PageChooserBlock(
        required=False, help_text="The page to redirect to once the order has finished."
    )

    class Meta:
        icon = "form"
        template = "wagtailpages/blocks/tito_widget_block.html"
