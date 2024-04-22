# Generated by Django 4.2.9 on 2024-02-01 18:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailpages", "0121_alter_productupdates_update"),
    ]

    operations = [
        migrations.AlterField(
            model_name="productupdates",
            name="update",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="product_pages",
                to="wagtailpages.update",
            ),
        ),
    ]
