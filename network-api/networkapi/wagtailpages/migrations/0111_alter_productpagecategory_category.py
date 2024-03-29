# Generated by Django 3.2.21 on 2023-10-23 16:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailpages", "0110_alter_articlepage_body"),
    ]

    operations = [
        migrations.AlterField(
            model_name="productpagecategory",
            name="category",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="product_pages",
                to="wagtailpages.buyersguideproductcategory",
            ),
        ),
    ]
