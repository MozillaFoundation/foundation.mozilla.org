# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-05-07 15:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailpages', '0019_auto_20180426_2213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modularpage',
            name='zen_nav',
            field=models.BooleanField(default=True, help_text='For secondary nav pages, use this to collapse the primary nav under a toggle hamburger.'),
        ),
    ]
