# Generated by Django 2.2.17 on 2021-04-08 19:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('highlights', '0003_highlight_image_new'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='highlight',
            name='image',
        ),
        migrations.RenameField(
            model_name='highlight',
            old_name='image_new',
            new_name='image',
        ),
    ]
