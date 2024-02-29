# Generated by Django 4.2.10 on 2024-02-27 12:28
from django.db import migrations
from wagtail.blocks.migrations.migrate_operation import MigrateStreamData

from networkapi.utility.migrations.operations import (
    AlterStreamChildBlockDataOperation,
)


def migrate_linkbuttonblock(source_block):
    return {
        **source_block,
        "value": {
            "label": source_block["value"]["label"],
            "URL": source_block["value"]["URL"],
            "styling": source_block["value"]["styling"],
            "link": {
                "file": None,
                "page": None,
                "email": "",
                "phone": "",
                "anchor": "",
                "link_to": "custom_url",
                "custom_url": source_block["value"]["URL"],
                "new_window": False,
            },
        },
    }


class Migration(migrations.Migration):

    dependencies = [
        ("donate", "0006_add_linkblock_to_linkbuttonblock"),
        ("wagtailcore", "0089_log_entry_data_json_null_to_object"),
    ]

    operations = [
        MigrateStreamData(
            app_name="donate",
            model_name="DonateHelpPage",
            field_name="body",
            operations_and_block_paths=[
                (AlterStreamChildBlockDataOperation(block="linkbutton", operation=migrate_linkbuttonblock), ""),
                (
                    AlterStreamChildBlockDataOperation(block="linkbutton", operation=migrate_linkbuttonblock),
                    "block_with_aside.aside",
                ),
            ],
        ),
    ]
