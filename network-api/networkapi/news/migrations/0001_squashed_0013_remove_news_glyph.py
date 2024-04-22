# Generated by Django 1.11.14 on 2018-07-26 03:52

from django.db import migrations, models

import networkapi.news.models


class Migration(migrations.Migration):
    replaces = [
        ("news", "0001_initial"),
        ("news", "0002_auto_20170322_1724"),
        ("news", "0003_auto_20170322_1912"),
        ("news", "0004_auto_20170327_1752"),
        ("news", "0005_news_excerpt"),
        ("news", "0006_auto_20170406_1855"),
        ("news", "0007_auto_20170504_2058"),
        ("news", "0008_auto_20170723_0853"),
        ("news", "0009_news_homepage"),
        ("news", "0010_remove_news_homepage"),
        ("news", "0011_auto_20171012_1326"),
        ("news", "0012_nullify_homepage"),
        ("news", "0013_remove_news_glyph"),
    ]

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="News",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "headline",
                    models.CharField(
                        help_text="Title of the article, post or media clip",
                        max_length=300,
                    ),
                ),
                (
                    "outlet",
                    models.CharField(help_text="Source of the article or media clip", max_length=300),
                ),
                ("date", models.DateField(help_text="Publish date of the media")),
                (
                    "link",
                    models.URLField(help_text="URL link to the article/media clip", max_length=500),
                ),
                (
                    "author",
                    models.CharField(
                        blank=True,
                        help_text="Name of the author of this news clip",
                        max_length=300,
                        null=True,
                    ),
                ),
                (
                    "featured",
                    models.BooleanField(
                        default=False,
                        help_text="Do you want to feature this news piece on the homepage?",
                    ),
                ),
                (
                    "excerpt",
                    models.TextField(
                        blank=True,
                        help_text="A short summary of the article (around 146 characters)",
                        max_length=200,
                        null=True,
                    ),
                ),
                (
                    "expires",
                    models.DateTimeField(
                        blank=True,
                        default=None,
                        help_text="Hide this news after this date and time (UTC)",
                        null=True,
                    ),
                ),
                (
                    "publish_after",
                    models.DateTimeField(
                        help_text="Make this news visible only after this date and time (UTC)",
                        null=True,
                    ),
                ),
                (
                    "is_video",
                    models.BooleanField(default=False, help_text="Is this news piece a video?"),
                ),
                (
                    "thumbnail",
                    models.FileField(
                        blank=True,
                        help_text="Thumbnail image associated with the news piece. Unsure of what to use? Leave blank and ask a designer",
                        max_length=2048,
                        null=True,
                        upload_to=networkapi.news.models.get_thumbnail_upload_path,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "news",
                "ordering": ("-date",),
                "verbose_name": "news article",
            },
        ),
    ]
