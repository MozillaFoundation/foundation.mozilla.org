# Generated by Django 2.2.16 on 2020-10-13 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buyersguide', '0003_auto_20201005_2317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generalproduct',
            name='data_control_policy_is_bad',
            field=models.BooleanField(default=False, verbose_name='Privacy ding'),
        ),
        migrations.AlterField(
            model_name='generalproduct',
            name='track_record_is_bad',
            field=models.BooleanField(default=False, verbose_name='Privacy ding'),
        ),
        migrations.AlterField(
            model_name='product',
            name='data_collection_policy_is_bad',
            field=models.BooleanField(default=False, verbose_name='Privacy ding'),
        ),
        migrations.AlterField(
            model_name='product',
            name='show_ding_for_minimum_security_standards',
            field=models.BooleanField(default=False, verbose_name='Privacy ding'),
        ),

        # soft-squash: 0005
        migrations.AlterModelOptions(
            name='buyersguideproductcategory',
            options={'ordering': ['sort_order', 'name'], 'verbose_name': 'Buyers Guide Product Category', 'verbose_name_plural': 'Buyers Guide Product Categories'},
        ),
        migrations.AddField(
            model_name='buyersguideproductcategory',
            name='sort_order',
            field=models.IntegerField(default=1, help_text='Sort ordering number - same-numbered items sort alphabetically'),
        ),

        # soft-squash: 0006
        migrations.AlterField(
            model_name='buyersguideproductcategory',
            name='sort_order',
            field=models.IntegerField(default=1, help_text='Sort ordering number. Same-numbered items sort alphabetically'),
        ),
    ]
