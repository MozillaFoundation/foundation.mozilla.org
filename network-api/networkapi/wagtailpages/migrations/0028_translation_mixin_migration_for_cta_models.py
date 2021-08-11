# Generated by Django 3.1.11 on 2021-06-10 18:23

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0062_comment_models_and_pagesubscription'),
        ('wagtailpages', '0027_bootstrap_subclassed_cta_models'),
    ]

    operations = [
        migrations.AlterField(
            model_name='petition',
            name='locale',
            field=models.ForeignKey(default=1, editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='wagtailcore.locale'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='petition',
            name='translation_key',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='signup',
            name='locale',
            field=models.ForeignKey(default=1, editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='wagtailcore.locale'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='signup',
            name='translation_key',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AlterUniqueTogether(
            name='petition',
            unique_together={('translation_key', 'locale')},
        ),
        migrations.AlterUniqueTogether(
            name='signup',
            unique_together={('translation_key', 'locale')},
        ),
    ]
