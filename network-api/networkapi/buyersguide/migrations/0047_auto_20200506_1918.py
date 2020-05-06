# Generated by Django 2.2.12 on 2020-05-06 19:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('buyersguide', '0046_auto_20200427_2322'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booleanvote',
            name='product',
        ),
        migrations.RemoveField(
            model_name='booleanvotebreakdown',
            name='product_vote',
        ),
        migrations.RemoveField(
            model_name='product',
            name='product_category',
        ),
        migrations.RemoveField(
            model_name='product',
            name='related_products',
        ),
        migrations.RemoveField(
            model_name='product',
            name='updates',
        ),
        migrations.RemoveField(
            model_name='productprivacypolicylink',
            name='product',
        ),
        migrations.RemoveField(
            model_name='rangeproductvote',
            name='product',
        ),
        migrations.RemoveField(
            model_name='rangevote',
            name='product',
        ),
        migrations.RemoveField(
            model_name='rangevotebreakdown',
            name='product_vote',
        ),
        migrations.DeleteModel(
            name='BooleanProductVote',
        ),
        migrations.DeleteModel(
            name='BooleanVote',
        ),
        migrations.DeleteModel(
            name='BooleanVoteBreakdown',
        ),
        migrations.DeleteModel(
            name='Product',
        ),
        migrations.DeleteModel(
            name='ProductPrivacyPolicyLink',
        ),
        migrations.DeleteModel(
            name='RangeProductVote',
        ),
        migrations.DeleteModel(
            name='RangeVote',
        ),
        migrations.DeleteModel(
            name='RangeVoteBreakdown',
        ),
    ]
