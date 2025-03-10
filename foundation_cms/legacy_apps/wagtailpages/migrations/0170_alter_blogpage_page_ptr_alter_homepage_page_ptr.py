# Generated by Django 4.2.16 on 2025-03-10 13:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailcore", "0094_alter_page_locale"),
        ("wagtailpages", "0169_alter_blogpage_body_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blogpage",
            name="page_ptr",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                parent_link=True,
                primary_key=True,
                related_name="legacy_blogpage",
                serialize=False,
                to="wagtailcore.page",
            ),
        ),
        migrations.AlterField(
            model_name="homepage",
            name="page_ptr",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                parent_link=True,
                primary_key=True,
                related_name="legacy_homepage",
                serialize=False,
                to="wagtailcore.page",
            ),
        ),
    ]
