# Generated by Django 4.2.9 on 2024-01-23 17:52

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailpages", "0119_alter_banneredcampaigntag_tag_alter_blogpagetag_tag"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="petition",
            options={"ordering": ["-id"], "verbose_name": "Petition"},
        ),
    ]
