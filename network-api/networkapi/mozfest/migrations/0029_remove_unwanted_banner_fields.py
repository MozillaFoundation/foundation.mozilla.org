# Generated by Django 3.2.23 on 2023-12-08 16:24

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("mozfest", "0028_mozfestlandingpage"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="mozfesthomepage",
            name="banner_carousel",
        ),
        migrations.RemoveField(
            model_name="mozfesthomepage",
            name="banner_cta_label",
        ),
        migrations.RemoveField(
            model_name="mozfesthomepage",
            name="banner_guide_text",
        ),
        migrations.RemoveField(
            model_name="mozfesthomepage",
            name="banner_video",
        ),
        migrations.RemoveField(
            model_name="mozfesthomepage",
            name="banner_video_url",
        ),
    ]