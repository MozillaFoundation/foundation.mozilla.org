from django.db import migrations
from wagtail.blocks.migrations.migrate_operation import MigrateStreamData

from foundation_cms.base.utils.data_migrations.callout_card_migration import (
    CALLOUT_CARD_OPERATIONS_AND_BLOCK_PATHS,
)


class Migration(migrations.Migration):
    dependencies = [
        ("gallery_hub", "0013_alter_projectpage_body"),
    ]

    operations = [
        MigrateStreamData(
            app_name="gallery_hub",
            model_name="ProjectPage",
            field_name="body",
            operations_and_block_paths=CALLOUT_CARD_OPERATIONS_AND_BLOCK_PATHS,
            chunk_size=1024,
        ),
    ]
