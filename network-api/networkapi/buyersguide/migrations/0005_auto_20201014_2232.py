# Generated by Django 2.2.16 on 2020-10-14 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buyersguide', '0004_auto_20201013_2034'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='buyersguideproductcategory',
            options={'ordering': ['sort_order', 'name'], 'verbose_name': 'Buyers Guide Product Category', 'verbose_name_plural': 'Buyers Guide Product Categories'},
        ),
        migrations.AddField(
            model_name='buyersguideproductcategory',
            name='sort_order',
            field=models.IntegerField(default=1, help_text='Sort ordering number - same-numbered items sort alphabetically'),
        ),
    ]
