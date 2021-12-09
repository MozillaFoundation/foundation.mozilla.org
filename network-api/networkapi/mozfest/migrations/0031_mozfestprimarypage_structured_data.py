# Generated by Django 3.1.11 on 2021-12-09 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mozfest', '0030_auto_20211202_1622'),
    ]

    operations = [
        migrations.AddField(
            model_name='mozfestprimarypage',
            name='structured_data',
            field=models.TextField(blank=True, help_text='Structured data JSON for Google search results. Do not include the <script> tag. See https://schema.org/ for properties and https://validator.schema.org/ to test validity.', null=True),
        ),
    ]
