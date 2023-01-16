# Generated by Django 3.2.13 on 2022-08-05 16:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailpages", "0043_add_buyersguidearticlepage_details_and_relations"),
    ]

    operations = [
        migrations.AddField(
            model_name="buyersguidepage",
            name="hero_featured_article",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="wagtailpages.buyersguidearticlepage",
            ),
        ),
        migrations.AlterField(
            model_name="buyersguidepage",
            name="intro_text",
            field=models.TextField(
                blank=True,
                help_text="A short blurb to show at the top of the page.",
                max_length=500,
            ),
        ),
    ]
