# Generated by Django 4.2.14 on 2024-08-02 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailpages", "0155_homepagetakeactioncards_cta"),
    ]

    operations = [
        migrations.AddField(
            model_name="homepage",
            name="show_hero_button",
            field=models.BooleanField(default=True, help_text="Display hero button"),
        ),
        migrations.AlterField(
            model_name="homepage",
            name="hero_headline",
            field=models.CharField(blank=True, help_text="Hero story headline", max_length=120),
        ),
    ]
