# Generated by Django 3.2.23 on 2023-12-14 14:37

import uuid

import django.db.models.deletion
import wagtail.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailcore", "0078_referenceindex"),
        ("mozfest", "0033_adds_image_and_text_carousel"),
    ]

    operations = [
        migrations.CreateModel(
            name="Ticket",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("translation_key", models.UUIDField(default=uuid.uuid4, editable=False)),
                ("name", models.CharField(help_text="Identify this ticket for other editors", max_length=100)),
                ("cost", models.CharField(help_text="E.g. €100.00", max_length=10)),
                ("group", models.CharField(blank=True, help_text="E.g Mega Patrons", max_length=50)),
                ("description", wagtail.fields.RichTextField(blank=True)),
                ("link_text", models.CharField(blank=True, help_text="E.G. Get tickets", max_length=25)),
                ("link_url", models.URLField(blank=True)),
                ("sticker_text", models.CharField(blank=True, help_text="Max 25 characters", max_length=25)),
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
                "verbose_name": "Ticket",
                "ordering": ["name"],
                "abstract": False,
                "unique_together": {("translation_key", "locale")},
            },
        ),
    ]
