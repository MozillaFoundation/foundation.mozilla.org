# Generated by Django 3.2.20 on 2023-09-04 18:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailpages", "0099_add_cta_aside_field_to_libraries_landing_page"),
    ]

    operations = [
        migrations.AddField(
            model_name="petition",
            name="show_comment_field",
            field=models.BooleanField(
                default=False, help_text="This toggles the visibility of the optional comment field."
            ),
        ),
        migrations.AddField(
            model_name="petition",
            name="show_country_field",
            field=models.BooleanField(
                default=False, help_text="This toggles the visibility of the optional country dropdown field."
            ),
        ),
        migrations.AddField(
            model_name="petition",
            name="show_postal_code_field",
            field=models.BooleanField(
                default=False, help_text="This toggles the visibility of the optional postal code field."
            ),
        ),
    ]
