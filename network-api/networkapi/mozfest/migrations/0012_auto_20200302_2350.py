# Generated by Django 2.2.10 on 2020-03-02 23:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mozfest', '0011_auto_20200220_0027'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mozfesthomepage',
            name='prefooter_text',
        ),
        migrations.RemoveField(
            model_name='mozfesthomepage',
            name='prefooter_text_de',
        ),
        migrations.RemoveField(
            model_name='mozfesthomepage',
            name='prefooter_text_en',
        ),
        migrations.RemoveField(
            model_name='mozfesthomepage',
            name='prefooter_text_es',
        ),
        migrations.RemoveField(
            model_name='mozfesthomepage',
            name='prefooter_text_fr',
        ),
        migrations.RemoveField(
            model_name='mozfesthomepage',
            name='prefooter_text_nl',
        ),
        migrations.RemoveField(
            model_name='mozfesthomepage',
            name='prefooter_text_pl',
        ),
        migrations.RemoveField(
            model_name='mozfesthomepage',
            name='prefooter_text_pt',
        ),
    ]
