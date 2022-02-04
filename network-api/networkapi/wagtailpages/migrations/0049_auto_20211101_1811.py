# Generated by Django 3.1.11 on 2021-11-01 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailpages', '0048_auto_20211103_1531'),
    ]

    operations = [
        migrations.AddField(
            model_name='callpower',
            name='share_email',
            field=models.CharField(blank=True, help_text='Share Progress id for email button, including the sp_... prefix', max_length=20),
        ),
        migrations.AddField(
            model_name='callpower',
            name='share_facebook',
            field=models.CharField(blank=True, help_text='Share Progress id for facebook button, including the sp_... prefix', max_length=20),
        ),
        migrations.AddField(
            model_name='callpower',
            name='share_twitter',
            field=models.CharField(blank=True, help_text='Share Progress id for twitter button, including the sp_... prefix', max_length=20),
        ),
    ]
