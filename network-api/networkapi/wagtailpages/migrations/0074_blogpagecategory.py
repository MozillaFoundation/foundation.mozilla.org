# Generated by Django 2.2.4 on 2019-08-29 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailpages', '0073_indexpage_page_size'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPageCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
    ]
