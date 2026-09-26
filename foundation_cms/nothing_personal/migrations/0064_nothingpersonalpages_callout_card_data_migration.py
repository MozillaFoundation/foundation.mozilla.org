from django.db import migrations
from wagtail.blocks.migrations.migrate_operation import MigrateStreamData

from foundation_cms.base.utils.data_migrations.callout_card_migration import (
    CALLOUT_CARD_OPERATIONS_AND_BLOCK_PATHS,
)

NOTHING_PERSONAL_MODELS = [
    "NothingPersonalArticleCollectionPage",
    "NothingPersonalArticlePage",
    "NothingPersonalPodcastPage",
    "NothingPersonalProductCollectionPage",
]


class Migration(migrations.Migration):
    dependencies = [
        ("nothing_personal", "0063_alter_nothingpersonalarticlecollectionpage_body_and_more"),
    ]

    operations = [
        MigrateStreamData(
            app_name="nothing_personal",
            model_name=model_name,
            field_name="body",
            operations_and_block_paths=CALLOUT_CARD_OPERATIONS_AND_BLOCK_PATHS,
            chunk_size=1024,
        )
        for model_name in NOTHING_PERSONAL_MODELS
    ]
