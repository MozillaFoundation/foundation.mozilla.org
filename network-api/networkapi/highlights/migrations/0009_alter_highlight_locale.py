# Generated by Django 4.2.16 on 2024-12-30 18:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailcore", "0094_alter_page_locale"),
        ("highlights", "0008_auto_20211209_0002"),
    ]

    operations = [
        migrations.AlterField(
            model_name="highlight",
            name="locale",
            field=models.ForeignKey(
                editable=False,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="wagtailcore.locale",
                verbose_name="locale",
            ),
        ),
    ]
