# Generated by Django 3.1.11 on 2021-10-28 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mozfest', '0023_auto_20211019_0025'),
    ]

    operations = [
        migrations.AddField(
            model_name='mozfesthomepage',
            name='banner_cta_label',
            field=models.CharField(blank=True, help_text='The label for the CTA that scrolls down to the banner video when clicked', max_length=250),
        ),
    ]
