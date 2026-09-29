"""Experimental Section Master field definition; no content conversion.

Reuse the frozen preceding migration, not the live registry. This avoids
repeating its unchanged block definitions while keeping the spike reproducible.
"""

from copy import deepcopy
from importlib import import_module

from django.db import migrations
from wagtail.fields import StreamField

previous = import_module("foundation_cms.core.migrations.0089_alter_generalpage_body")
_, _, field_args, field_kwargs = previous.Migration.operations[0].field.deconstruct()
field_args, field_kwargs = deepcopy((field_args, field_kwargs))
field_args[0].append(("section_master", 175))
field_kwargs["block_lookup"].update(
    {
        171: ("wagtail.blocks.CharBlock", (), {"help_text": "Editor-only section label.", "required": False}),
        172: (
            "wagtail.blocks.ChoiceBlock",
            [],
            {"choices": [("none", "None"), ("regular", "Regular"), ("generous", "Generous")]},
        ),
        173: (
            "wagtail.blocks.ChoiceBlock",
            [],
            {"choices": [("compact", "Compact"), ("regular", "Regular"), ("relaxed", "Relaxed")]},
        ),
        174: (
            "wagtail.blocks.StreamBlock",
            [
                [
                    ("rich_text", 116),
                    ("title_block", 165),
                    ("quote", 115),
                    ("link_button_block", 89),
                    ("image", 62),
                    ("image_grid", 82),
                    ("accordion_block", 5),
                    ("list_block", 94),
                    ("two_column_container_block", 169),
                    ("three_column_container_block", 156),
                ]
            ],
            {"required": False},
        ),
        175: (
            "wagtail.blocks.StructBlock",
            [[("label", 171), ("padding", 172), ("rhythm", 173), ("content", 174)]],
            {},
        ),
    }
)


class Migration(migrations.Migration):
    dependencies = [("core", "0089_alter_generalpage_body")]

    operations = [
        migrations.AlterField(
            model_name="generalpage",
            name="body",
            field=StreamField(*field_args, **field_kwargs),
        ),
    ]
