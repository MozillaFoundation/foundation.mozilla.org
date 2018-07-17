# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-07-17 18:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0019_delete_filter'),
        ('wagtailpages', '0037_initiativespage_subheader'),
    ]

    operations = [
        migrations.AddField(
            model_name='initiativesection',
            name='sectionImage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='section_image', to='wagtailimages.Image'),
        ),
    ]
