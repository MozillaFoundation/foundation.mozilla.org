# Generated by Django 2.2.17 on 2021-03-02 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailpages', '0040_auto_20210227_0528'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlepage',
            name='show_side_share_buttons',
            field=models.BooleanField(default=True, help_text='Show social share buttons on the side'),
        ),
    ]
