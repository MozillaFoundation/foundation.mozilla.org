# Generated by Django 4.2.10 on 2024-02-27 12:28
from django.db import migrations
from wagtail.blocks.migrations.migrate_operation import MigrateStreamData

from foundation_cms.legacy_cms.utility.migration.operations import AlterStreamChildBlockDataOperation


def migrate_linkbuttonblock(source_block):
    source_block["value"]["relative_url"] = ""
    return source_block


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailpages", "0130_fix_urls_on_translation_context_model"),
        ("wagtailcore", "0089_log_entry_data_json_null_to_object"),
    ]

    operations = [
        MigrateStreamData(
            app_name="wagtailpages",
            model_name="ArticlePage",
            field_name="body",
            operations_and_block_paths=[
                (AlterStreamChildBlockDataOperation(block="linkbutton", operation=migrate_linkbuttonblock), ""),
            ],
        ),
        MigrateStreamData(
            app_name="wagtailpages",
            model_name="BlogPage",
            field_name="body",
            operations_and_block_paths=[
                (AlterStreamChildBlockDataOperation(block="linkbutton", operation=migrate_linkbuttonblock), ""),
                (
                    AlterStreamChildBlockDataOperation(block="linkbutton", operation=migrate_linkbuttonblock),
                    "block_with_aside.aside",
                ),
            ],
        ),
        MigrateStreamData(
            app_name="wagtailpages",
            model_name="BuyersGuideArticlePage",
            field_name="body",
            operations_and_block_paths=[
                (AlterStreamChildBlockDataOperation(block="linkbutton", operation=migrate_linkbuttonblock), ""),
            ],
        ),
        MigrateStreamData(
            app_name="wagtailpages",
            model_name="BuyersGuideCampaignPage",
            field_name="body",
            operations_and_block_paths=[
                (AlterStreamChildBlockDataOperation(block="linkbutton", operation=migrate_linkbuttonblock), ""),
            ],
        ),
        MigrateStreamData(
            app_name="wagtailpages",
            model_name="ModularPage",
            field_name="body",
            operations_and_block_paths=[
                (AlterStreamChildBlockDataOperation(block="linkbutton", operation=migrate_linkbuttonblock), ""),
                (
                    AlterStreamChildBlockDataOperation(block="linkbutton", operation=migrate_linkbuttonblock),
                    "block_with_aside.aside",
                ),
            ],
        ),
        MigrateStreamData(
            app_name="wagtailpages",
            model_name="PrimaryPage",
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
