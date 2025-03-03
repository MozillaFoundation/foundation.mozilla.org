# Generated by Django 4.2.14 on 2024-07-22 14:02
from django.db import migrations
from wagtail.blocks.migrations.migrate_operation import MigrateStreamData

from foundation_cms.legacy_cms.utility.migration.operations import AlterStreamChildBlockDataOperation


def format_image_grid_block_items_empty_values(source_block):
    if "grid_items" in source_block["value"]:
        for item in source_block["value"]["grid_items"]:
            item_value = item.get("value", item)
            link_value = item_value.get("link", None)

            if not link_value:
                item_value["link"] = []

    return source_block


def format_image_teaser_block_empty_value(source_block):
    link_button_value = source_block["value"].get("link_button", None)

    if not link_button_value:
        source_block["value"]["link_button"] = []

    return source_block


def format_group_listing_block_cards_empty_values(source_block):
    if "cards" in source_block["value"]:
        for card in source_block["value"]["cards"]:
            card_value = card.get("value", card)
            link_value = card_value.get("link", None)

            if not link_value:
                card_value["link"] = []

    return source_block


class Migration(migrations.Migration):

    dependencies = [
        ("mozfest", "0061_update_textonlyteaserblock_with_linkblock"),
    ]

    operations = [
        MigrateStreamData(
            app_name="mozfest",
            model_name="mozfestprimarypage",
            field_name="body",
            operations_and_block_paths=[
                (
                    AlterStreamChildBlockDataOperation(
                        block="image_grid", operation=format_image_grid_block_items_empty_values
                    ),
                    "",
                ),
                (
                    AlterStreamChildBlockDataOperation(
                        block="image_teaser_block", operation=format_image_teaser_block_empty_value
                    ),
                    "",
                ),
                (
                    AlterStreamChildBlockDataOperation(
                        block="group_listing_block", operation=format_group_listing_block_cards_empty_values
                    ),
                    "",
                ),
            ],
        ),
    ]
