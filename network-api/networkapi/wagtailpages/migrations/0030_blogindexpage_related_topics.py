# Generated by Django 3.2.13 on 2022-06-21 05:07

from django.db import migrations
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailpages', '0029_featuredvideopost'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogindexpage',
            name='related_topics',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, help_text='Which topics would you like to feature on the page? Please select a max of 7.', to='wagtailpages.BlogPageTopic', verbose_name='Topics'),
        ),
    ]
