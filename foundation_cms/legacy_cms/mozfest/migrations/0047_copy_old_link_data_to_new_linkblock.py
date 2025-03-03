# Generated by Django 4.2.10 on 2024-02-27 12:28
from django.db import migrations
from wagtail.blocks.migrations.migrate_operation import MigrateStreamData

from foundation_cms.legacy_cms.utility.migration.operations import AlterStreamChildBlockDataOperation


def migrate_linkbuttonblock(source_block):
    """Copy old link data to new LinkBlock inside a LinkButtonBlock."""
    return {
        **source_block,
        "value": {
            "label": source_block["value"]["label"],
            "URL": source_block["value"]["URL"],
            "styling": source_block["value"]["styling"],
            "file": None,
            "page": None,
            "email": "",
            "phone": "",
            "anchor": "",
            "link_to": "external_url",
            "external_url": source_block["value"]["URL"],
            "new_window": False,
        },
    }


def migrate_ctablock(source_block):
    """Copy old link data to LinkBlock inside a CTABlock."""
    return {
        **source_block,
        "value": {
            "heading": source_block["value"]["heading"],
            "text": source_block["value"]["text"],
            "link_url": source_block["value"]["link_url"],
            "link_text": source_block["value"]["link_text"],
            "dark_background": source_block["value"]["dark_background"],
            "file": None,
            "page": None,
            "email": "",
            "phone": "",
            "anchor": "",
            "link_to": "external_url",
            "external_url": source_block["value"]["link_url"],
            "new_window": False,
            "label": source_block["value"]["link_text"],
        },
    }


class Migration(migrations.Migration):

    dependencies = [
        ("mozfest", "0046_add_target_linkblock_to_linkbuttonblock_and_ctablock"),
        ("wagtailcore", "0089_log_entry_data_json_null_to_object"),
    ]

    operations = [
        MigrateStreamData(
            app_name="mozfest",
            model_name="MozfestPrimaryPage",
            field_name="body",
            operations_and_block_paths=[
                (AlterStreamChildBlockDataOperation(block="linkbutton", operation=migrate_linkbuttonblock), ""),
                (
                    AlterStreamChildBlockDataOperation(block="linkbutton", operation=migrate_linkbuttonblock),
                    "block_with_aside.aside",
                ),
                (AlterStreamChildBlockDataOperation(block="cta", operation=migrate_ctablock), ""),
            ],
        ),
        MigrateStreamData(
            app_name="mozfest",
            model_name="MozfestHomepage",
            field_name="body",
            operations_and_block_paths=[
                (AlterStreamChildBlockDataOperation(block="linkbutton", operation=migrate_linkbuttonblock), ""),
                (
                    AlterStreamChildBlockDataOperation(block="linkbutton", operation=migrate_linkbuttonblock),
                    "block_with_aside.aside",
                ),
                (AlterStreamChildBlockDataOperation(block="cta", operation=migrate_ctablock), ""),
            ],
        ),
        MigrateStreamData(
            app_name="mozfest",
            model_name="MozfestLandingPage",
            field_name="body",
            operations_and_block_paths=[
                (AlterStreamChildBlockDataOperation(block="linkbutton", operation=migrate_linkbuttonblock), ""),
                (
                    AlterStreamChildBlockDataOperation(block="linkbutton", operation=migrate_linkbuttonblock),
                    "block_with_aside.aside",
                ),
                (AlterStreamChildBlockDataOperation(block="cta", operation=migrate_ctablock), ""),
            ],
        ),
    ]
