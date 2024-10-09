# Generated by Django 4.2.15 on 2024-10-07 21:41

from django.db import migrations, models

import networkapi.wagtailpages.fields


def map_yes_no_to_cant_determine(apps, schema_editor):
    GeneralProductPage = apps.get_model("wagtailpages", "GeneralProductPage")

    # Filter all instances where 'ai_is_untrustworthy' is 'Yes' or 'No'
    pages_to_update = GeneralProductPage.objects.filter(ai_is_untrustworthy__in=["Yes", "No"])

    # Iterate over the pages and update them
    for page in pages_to_update:
        page.ai_is_untrustworthy = "CD"
        page.save()


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailpages", "0166_homepagehighlights_replace_homepagenewsyoucanuse"),
    ]

    operations = [
        migrations.AlterField(
            model_name="generalproductpage",
            name="ai_is_untrustworthy",
            field=networkapi.wagtailpages.fields.ExtendedChoiceField(verbose_name="How trustworthy is the AI?"),
        ),
        migrations.AddField(
            model_name="generalproductpage",
            name="ai_is_untrustworthy_helptext",
            field=models.TextField(blank=True, max_length=5000, verbose_name="How trustworthy is the AI explanation"),
        ),
        migrations.RunPython(map_yes_no_to_cant_determine),
    ]
