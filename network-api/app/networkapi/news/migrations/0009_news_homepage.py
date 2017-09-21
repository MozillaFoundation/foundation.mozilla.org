# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-31 17:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0001_initial'),
        ('news', '0008_auto_20170723_0853'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='homepage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='news', to='homepage.Homepage'),
        ),
    ]
