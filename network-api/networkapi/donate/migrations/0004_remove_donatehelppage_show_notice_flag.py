# Generated by Django 3.2.21 on 2023-10-06 18:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('donate', '0003_donatehelppage_show_notice'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='donatehelppage',
            name='show_notice',
        ),
    ]
