# Generated by Django 2.2.16 on 2020-10-15 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buyersguide', '0005_auto_20201014_2232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyersguideproductcategory',
            name='sort_order',
            field=models.IntegerField(default=1, help_text='Sort ordering number. Same-numbered items sort alphabetically'),
        ),
    ]
