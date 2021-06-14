# Generated by Django 3.1.11 on 2021-05-31 18:02

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0062_comment_models_and_pagesubscription'),
        ('news', '0006_bootstrap_migration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='locale',
            field=models.ForeignKey(default=1, editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='wagtailcore.locale'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='news',
            name='translation_key',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AlterUniqueTogether(
            name='news',
            unique_together={('translation_key', 'locale')},
        ),
    ]
