# Generated by Django 4.2.20 on 2025-07-15 19:55

import wagtail.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("mozfest", "0071_add_source_to_tickets_block"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="mozfesthomepage",
            name="banner_link_text",
        ),
        migrations.RemoveField(
            model_name="mozfesthomepage",
            name="banner_link_url",
        ),
        migrations.RemoveField(
            model_name="mozfesthomepage",
            name="cta_button_destination",
        ),
        migrations.RemoveField(
            model_name="mozfesthomepage",
            name="cta_button_label",
        ),
        migrations.RemoveField(
            model_name="mozfestlandingpage",
            name="banner_link_text",
        ),
        migrations.RemoveField(
            model_name="mozfestlandingpage",
            name="banner_link_url",
        ),
        migrations.AddField(
            model_name="mozfesthomepage",
            name="banner_cta",
            field=wagtail.fields.StreamField(
                [("tito_widget", 5)],
                blank=True,
                block_lookup={
                    0: ("wagtail.blocks.CharBlock", (), {"help_text": "The text to show on the Tito button."}),
                    1: (
                        "wagtail.blocks.ChoiceBlock",
                        [],
                        {"choices": [("btn-primary", "Primary button"), ("btn-secondary", "Secondary button")]},
                    ),
                    2: (
                        "wagtail.snippets.blocks.SnippetChooserBlock",
                        ("events.TitoEvent",),
                        {"help_event": "The Tito event to be displayed"},
                    ),
                    3: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {
                            "help_text": 'Comma-separated list of ticket/release IDs to limit to, e.g. "3elajg6qcxu,6qiiw4socs4"',
                            "required": False,
                        },
                    ),
                    4: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {
                            "help_text": "Enter a source to track where events come from.",
                            "max_length": 255,
                            "required": False,
                        },
                    ),
                    5: (
                        "wagtail.blocks.StructBlock",
                        [[("button_label", 0), ("styling", 1), ("event", 2), ("releases", 3), ("source", 4)]],
                        {},
                    ),
                },
                verbose_name="Banner CTA",
            ),
        ),
        migrations.AddField(
            model_name="mozfesthomepage",
            name="nav_cta",
            field=wagtail.fields.StreamField(
                [("tito_widget", 5)],
                blank=True,
                block_lookup={
                    0: ("wagtail.blocks.CharBlock", (), {"help_text": "The text to show on the Tito button."}),
                    1: (
                        "wagtail.blocks.ChoiceBlock",
                        [],
                        {"choices": [("btn-primary", "Primary button"), ("btn-secondary", "Secondary button")]},
                    ),
                    2: (
                        "wagtail.snippets.blocks.SnippetChooserBlock",
                        ("events.TitoEvent",),
                        {"help_event": "The Tito event to be displayed"},
                    ),
                    3: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {
                            "help_text": 'Comma-separated list of ticket/release IDs to limit to, e.g. "3elajg6qcxu,6qiiw4socs4"',
                            "required": False,
                        },
                    ),
                    4: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {
                            "help_text": "Enter a source to track where events come from.",
                            "max_length": 255,
                            "required": False,
                        },
                    ),
                    5: (
                        "wagtail.blocks.StructBlock",
                        [[("button_label", 0), ("styling", 1), ("event", 2), ("releases", 3), ("source", 4)]],
                        {},
                    ),
                },
                verbose_name="Nav CTA",
            ),
        ),
        migrations.AddField(
            model_name="mozfestlandingpage",
            name="banner_cta",
            field=wagtail.fields.StreamField(
                [("tito_widget", 5)],
                blank=True,
                block_lookup={
                    0: ("wagtail.blocks.CharBlock", (), {"help_text": "The text to show on the Tito button."}),
                    1: (
                        "wagtail.blocks.ChoiceBlock",
                        [],
                        {"choices": [("btn-primary", "Primary button"), ("btn-secondary", "Secondary button")]},
                    ),
                    2: (
                        "wagtail.snippets.blocks.SnippetChooserBlock",
                        ("events.TitoEvent",),
                        {"help_event": "The Tito event to be displayed"},
                    ),
                    3: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {
                            "help_text": 'Comma-separated list of ticket/release IDs to limit to, e.g. "3elajg6qcxu,6qiiw4socs4"',
                            "required": False,
                        },
                    ),
                    4: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {
                            "help_text": "Enter a source to track where events come from.",
                            "max_length": 255,
                            "required": False,
                        },
                    ),
                    5: (
                        "wagtail.blocks.StructBlock",
                        [[("button_label", 0), ("styling", 1), ("event", 2), ("releases", 3), ("source", 4)]],
                        {},
                    ),
                },
                verbose_name="Banner CTA",
            ),
        ),
    ]
