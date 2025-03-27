# Generated by Django 4.2.20 on 2025-03-26 20:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("images", "0001_initial"),
        ("highlights", "0009_alter_highlight_locale"),
    ]

    operations = [
        migrations.AlterField(
            model_name="highlight",
            name="image",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.foundationcustomimage",
            ),
        ),
    ]
