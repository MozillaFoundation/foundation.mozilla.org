# Generated by Django 3.2.20 on 2023-08-08 12:39

import uuid

import django.db.models.deletion
import modelcluster.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailcore", "0078_referenceindex"),
        ("wagtailpages", "0094_alter_petition_campaign_id"),
    ]

    operations = [
        migrations.CreateModel(
            name="ResearchLandingPageFeaturedAuthorsRelation",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("translation_key", models.UUIDField(default=uuid.uuid4, editable=False)),
                ("sort_order", models.IntegerField(blank=True, editable=False, null=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="+", to="wagtailpages.profile"
                    ),
                ),
                (
                    "landing_page",
                    modelcluster.fields.ParentalKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="featured_authors",
                        to="wagtailpages.researchlandingpage",
                    ),
                ),
                (
                    "locale",
                    models.ForeignKey(
                        editable=False,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="wagtailcore.locale",
                    ),
                ),
            ],
            options={
                "abstract": False,
                "unique_together": {("translation_key", "locale")},
            },
        ),
        migrations.CreateModel(
            name="RCCLandingPageFeaturedAuthorsRelation",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("translation_key", models.UUIDField(default=uuid.uuid4, editable=False)),
                ("sort_order", models.IntegerField(blank=True, editable=False, null=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="+", to="wagtailpages.profile"
                    ),
                ),
                (
                    "landing_page",
                    modelcluster.fields.ParentalKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="featured_authors",
                        to="wagtailpages.rcclandingpage",
                    ),
                ),
                (
                    "locale",
                    models.ForeignKey(
                        editable=False,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="wagtailcore.locale",
                    ),
                ),
            ],
            options={
                "abstract": False,
                "unique_together": {("translation_key", "locale")},
            },
        ),
    ]
