# Generated by Django 4.2.11 on 2024-04-25 03:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailimages", "0025_alter_image_file_alter_rendition_file"),
        ("nav", "0003_add_blog_dropdown"),
    ]

    operations = [
        migrations.AlterField(
            model_name="navmenufeaturedblogtopicrelationship",
            name="icon",
            field=models.ForeignKey(
                help_text="Please use SVG format",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="wagtailimages.image",
                verbose_name="Icon",
            ),
        ),
    ]
