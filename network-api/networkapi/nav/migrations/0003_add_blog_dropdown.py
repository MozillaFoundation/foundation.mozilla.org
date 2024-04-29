# Generated by Django 4.2.11 on 2024-04-19 16:48

import uuid

import django.db.models.deletion
import modelcluster.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailimages", "0025_alter_image_file_alter_rendition_file"),
        ("wagtailpages", "0135_featuredcampaignpagerelation"),
        ("wagtailcore", "0089_log_entry_data_json_null_to_object"),
        ("nav", "0002_sitenavmenu"),
    ]

    operations = [
        migrations.AddField(
            model_name="navmenu",
            name="blog_button_label",
            field=models.CharField(blank=True, max_length=100, verbose_name="Blog button label"),
        ),
        migrations.AddField(
            model_name="navmenu",
            name="enable_blog_dropdown",
            field=models.BooleanField(default=False, verbose_name="Enable Blog Dropdown?"),
        ),
        migrations.CreateModel(
            name="NavMenuFeaturedBlogTopicRelationship",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("translation_key", models.UUIDField(default=uuid.uuid4, editable=False)),
                ("sort_order", models.IntegerField(blank=True, editable=False, null=True)),
                (
                    "icon",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="wagtailimages.image",
                        verbose_name="Icon",
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
                (
                    "menu",
                    modelcluster.fields.ParentalKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="featured_blog_topics",
                        to="nav.navmenu",
                        verbose_name="Navigation Menu",
                    ),
                ),
                (
                    "topic",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="nav_menu_featured_topics",
                        to="wagtailpages.blogpagetopic",
                        verbose_name="Featured Blog Topic",
                    ),
                ),
            ],
            options={
                "verbose_name": "Featured Blog Topic",
                "verbose_name_plural": "Featured Blog Topics",
                "ordering": ["sort_order"],
                "abstract": False,
                "unique_together": {("translation_key", "locale")},
            },
        ),
    ]
