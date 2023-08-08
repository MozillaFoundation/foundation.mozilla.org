# Generated by Django 3.2.16 on 2022-12-21 19:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailcore", "0066_collection_management_permissions"),
        ("wagtailpages", "0071_buyersguidepage_remove_outdated_fields"),
    ]

    operations = [
        migrations.AlterField(
            model_name="buyersguidecontentcategory",
            name="slug",
            field=models.SlugField(
                help_text="The slug is auto-generated from the title, but can be customized if needed. It needs to be unique per locale. ",
                max_length=100,
            ),
        ),
        migrations.AlterUniqueTogether(
            name="buyersguidecontentcategory",
            unique_together={("locale", "slug"), ("translation_key", "locale")},
        ),
    ]
