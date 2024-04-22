# Generated by Django 4.2.9 on 2024-02-02 15:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailpages", "0122_alter_productupdates_update"),
    ]

    operations = [
        migrations.AlterField(
            model_name="petition",
            name="show_comment_field",
            field=models.BooleanField(
                default=False,
                help_text="This toggles the visibility of the optional comment field.",
                verbose_name="Show comment field?",
            ),
        ),
        migrations.AlterField(
            model_name="petition",
            name="show_country_field",
            field=models.BooleanField(
                default=False,
                help_text="This toggles the visibility of the optional country dropdown field.",
                verbose_name="Show country field?",
            ),
        ),
        migrations.AlterField(
            model_name="petition",
            name="show_postal_code_field",
            field=models.BooleanField(
                default=False,
                help_text="This toggles the visibility of the optional postal code field.",
                verbose_name="Show postal code field?",
            ),
        ),
        migrations.AlterField(
            model_name="signup",
            name="ask_name",
            field=models.BooleanField(
                default=False, help_text="Check this box to show (optional) name fields", verbose_name="Ask for name?"
            ),
        ),
        migrations.AlterField(
            model_name="update",
            name="created_date",
            field=models.DateField(
                auto_now_add=True, help_text="The date this update was created", verbose_name="Created at"
            ),
        ),
        migrations.AlterField(
            model_name="update",
            name="featured",
            field=models.BooleanField(
                default=False, help_text="feature this update at the top of the list?", verbose_name="Featured?"
            ),
        ),
    ]
