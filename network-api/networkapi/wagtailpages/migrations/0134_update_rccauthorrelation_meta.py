# Generated by Django 4.2.11 on 2024-04-12 21:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailpages", "0133_appinstallpage"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="rccauthorrelation",
            options={"ordering": ["sort_order"]},
        ),
    ]
