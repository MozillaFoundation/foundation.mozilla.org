# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-07-20 20:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('highlights', '0007_nullify_homepage'),
        ('wagtailimages', '0019_delete_filter'),
        ('wagtailpages', '0032_auto_20180712_2234'),
    ]

    operations = [
        migrations.CreateModel(
            name='InitiativeSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sectionHeader', models.CharField(max_length=250, verbose_name='Header')),
                ('sectionCopy', models.TextField(verbose_name='Subheader')),
                ('sectionButtonTitle', models.CharField(max_length=250, verbose_name='Button Text')),
                ('sectionButtonURL', models.URLField(verbose_name='Button URL')),
            ],
        ),
        migrations.CreateModel(
            name='InitiativesHighlights',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('highlight', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='highlights.Highlight')),
            ],
            options={
                'verbose_name': 'highlight',
                'verbose_name_plural': 'highlights',
                'ordering': ['sort_order'],
            },
        ),
        migrations.AddField(
            model_name='initiativespage',
            name='h3',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='initiativespage',
            name='primaryHero',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='primary_hero', to='wagtailimages.Image', verbose_name='Primary Hero Image'),
        ),
        migrations.AddField(
            model_name='initiativespage',
            name='sub_h3',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='initiativespage',
            name='subheader',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='initiativeshighlights',
            name='page',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='featured_highlights', to='wagtailpages.InitiativesPage'),
        ),
        migrations.AddField(
            model_name='initiativesection',
            name='page',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='initiative_sections', to='wagtailpages.InitiativesPage'),
        ),
        migrations.AddField(
            model_name='initiativesection',
            name='sectionImage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='section_image', to='wagtailimages.Image', verbose_name='Hero Image'),
        ),
    ]
