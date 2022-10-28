# Generated by Django 3.2.16 on 2022-10-28 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailpages', '0053_add_streamfield_blocks'),
    ]

    operations = [
        migrations.AddField(
            model_name='banneredcampaignpage',
            name='use_intro_from_parent',
            field=models.BooleanField(default=False, help_text='This field will overwrite the intro field above with the intro field from this pages parent'),
        ),
    ]
