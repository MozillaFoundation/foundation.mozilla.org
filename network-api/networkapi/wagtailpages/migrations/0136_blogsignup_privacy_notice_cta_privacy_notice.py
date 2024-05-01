# Generated by Django 4.2.11 on 2024-04-30 18:33

import wagtail.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailpages", "0135_featuredcampaignpagerelation"),
    ]

    operations = [
        migrations.AddField(
            model_name="blogsignup",
            name="privacy_notice",
            field=wagtail.fields.RichTextField(
                blank=True,
                help_text="This optional privacy notice field will overwrite the default privacy notice text. If this field is left blank, the default privacy notice text is used.",
            ),
        ),
        migrations.AddField(
            model_name="cta",
            name="privacy_notice",
            field=wagtail.fields.RichTextField(
                blank=True,
                help_text="This optional privacy notice field will overwrite the default privacy notice text. If this field is left blank, the default privacy notice text is used.",
            ),
        ),
    ]