# Generated by Django 3.1.11 on 2021-09-23 19:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailpages', '0040_cta_refactor_3'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='banneredcampaignpage',
            name='petition_cta',
        ),
        migrations.RemoveField(
            model_name='campaignpage',
            name='petition_cta',
        ),
    ]
