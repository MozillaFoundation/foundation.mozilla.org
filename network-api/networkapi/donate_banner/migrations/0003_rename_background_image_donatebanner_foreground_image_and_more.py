# Generated by Django 4.2.15 on 2024-10-29 15:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailimages", "0025_alter_image_file_alter_rendition_file"),
        ("donate_banner", "0002_remove_cta_text_and_update_max_lengths"),
    ]
    # @see https://code.djangoproject.com/ticket/23577
    # Index should be dropped and recreated in order to add a field with the name of a previous indexed field
    operations = [
        migrations.AlterField(
            model_name="donatebanner",
            name="background_image",
            field=models.ForeignKey(
                blank=True,
                db_index=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="donate_banner.donatebanner",
            ),
        ),
        migrations.RenameField(
            model_name="donatebanner",
            old_name="background_image",
            new_name="foreground_image",
        ),
        migrations.AlterField(
            model_name="donatebanner",
            name="foreground_image",
            field=models.ForeignKey(
                blank=True,
                db_index=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="donate_banner.donatebanner",
            ),
        ),
    ]
