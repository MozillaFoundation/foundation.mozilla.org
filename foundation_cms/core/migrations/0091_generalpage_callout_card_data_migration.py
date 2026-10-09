from django.db import migrations
from wagtail.blocks.migrations.migrate_operation import MigrateStreamData
from wagtail.blocks.migrations.operations import (
    RemoveStructChildrenOperation,
    RenameStreamChildrenOperation,
    RenameStructChildrenOperation,
)


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0090_alter_generalpage_body_alter_homepage_body"),  # Previous Callout Card schema migration
    ]

    operations = [
        MigrateStreamData(
            app_name="core",
            model_name="GeneralPage",
            field_name="body",
            operations_and_block_paths=[
                (
                    RenameStreamChildrenOperation(old_name="card", new_name="callout_card"),
                    "timely_activations_cards.cards",
                ),
                (
                    RenameStructChildrenOperation(old_name="category", new_name="headline"),
                    "timely_activations_cards.cards.callout_card",
                ),
                (
                    RenameStructChildrenOperation(old_name="title", new_name="subheading"),
                    "timely_activations_cards.cards.callout_card",
                ),
                (
                    RenameStructChildrenOperation(old_name="text", new_name="body"),
                    "timely_activations_cards.cards.callout_card",
                ),
                (
                    RemoveStructChildrenOperation(name="link"),
                    "timely_activations_cards.cards.callout_card",
                ),
            ],
            chunk_size=1024,
        ),
        MigrateStreamData(
            app_name="core",
            model_name="homepage",
            field_name="body",
            operations_and_block_paths=[
                (
                    RenameStreamChildrenOperation(old_name="card", new_name="callout_card"),
                    "timely_activations_cards.cards",
                ),
                (
                    RenameStructChildrenOperation(old_name="category", new_name="headline"),
                    "timely_activations_cards.cards.callout_card",
                ),
                (
                    RenameStructChildrenOperation(old_name="title", new_name="subheading"),
                    "timely_activations_cards.cards.callout_card",
                ),
                (
                    RenameStructChildrenOperation(old_name="text", new_name="body"),
                    "timely_activations_cards.cards.callout_card",
                ),
                (
                    RemoveStructChildrenOperation(name="link"),
                    "timely_activations_cards.cards.callout_card",
                ),
            ],
            chunk_size=1024,
        ),
    ]
