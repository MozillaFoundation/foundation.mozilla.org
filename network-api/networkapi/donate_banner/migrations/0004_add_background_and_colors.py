# Generated by Django 4.2.15 on 2024-10-29 15:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailimages", "0025_alter_image_file_alter_rendition_file"),
        ("donate_banner", "0003_rename_background_image_donatebanner_foreground_image_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="donatebanner",
            name="background_color",
            field=models.CharField(
                choices=[
                    ("tw-bg-red-40", "Red"),
                    ("tw-bg-blue-40", "Blue"),
                    ("tw-bg-white", "White"),
                    ("tw-bg-black", "Black"),
                ],
                default="tw-bg-blue-40",
                help_text="Background color for the banner",
                max_length=20,
                null=True,
                blank=True,
            ),
        ),
        migrations.AddField(
            model_name="donatebanner",
            name="background_image",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="wagtailimages.image",
            ),
        ),
        migrations.AddField(
            model_name="donatebanner",
            name="text_color",
            field=models.CharField(
                choices=[("tw-text-white", "White"), ("tw-text-black", "Black")],
                default="tw-text-white",
                help_text="Text color for the banner",
                max_length=20,
            ),
        ),
    ]